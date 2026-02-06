import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import os
import json
import requests
import argparse
from datetime import datetime
from typing import Any, List, Optional
from urllib.request import urlopen, Request
from app.schemas.project_inspection import ProjectInspectionBase
from app.core.database import get_db
from app.models.product_inspection import ProductInspection
from app.models.molding_machine_state import MoldingMachineState
from app.models.object_detection import ObjectDetection
from app.models.defect import Defect
from app.models.pixel_severity import PixelSeverity

DEFAULT_URL = os.getenv("DATASET_URL", "https://static.krevera.com/dataset.json")

def _parse_timestamp(ts: Any) -> datetime:
    if isinstance(ts, (int, float)):
        return datetime.fromtimestamp(ts)
    if isinstance(ts, str):
        try:
            return datetime.fromisoformat(ts)
        except ValueError:
            try:
                return datetime.fromtimestamp(float(ts))
            except Exception as exc:
                raise ValueError(f"Unrecognized timestamp format: {ts}") from exc
    raise ValueError(f"Unrecognized timestamp type: {type(ts)}")


def _normalize_object_detections(raw: dict) -> dict:
    if "object_detections" in raw:
        detections = raw["object_detections"]
    elif "object_detection" in raw:
        od = raw["object_detection"]
        if isinstance(od, dict):
            detections = {"default": od}
        else:
            detections = {"default": od}
    else:
        return {}

    normalized = {}
    for name, od in detections.items():
        if not isinstance(od, dict):
            continue
        
        item = {
            "reject": od.get("reject", False),
            "label_detection": od.get("label_detection") or {},
        }
        
        for key, value in od.items():
            if key not in ("reject", "label_detection"):
                item[key] = value
        
        normalized[name] = item
    
    return normalized


def _prepare(raw: dict) -> dict:
    data = raw.copy()

    for key in list(data.keys()):
        if "-" in key:
            data[key.replace("-", "_")] = data.pop(key)

    if "timestamp" in data:
        data["timestamp"] = _parse_timestamp(data["timestamp"])

    if "molding_machine_state" not in data:
        data["molding_machine_state"] = {}

    data["object_detections"] = _normalize_object_detections(data)

    return data


def ingest_one(raw: dict, db_session=None) -> ProductInspection:
    created_session = False
    session = db_session

    if session is None:
        session = get_session()
        created_session = True

    try:
        prepared = _prepare(raw)
        validated = ProjectInspectionBase.model_validate(prepared)

        inspection = ProductInspection(
            version=validated.version,
            timestamp=validated.timestamp,
            molding_machine_id=validated.molding_machine_id,
        )
        session.add(inspection)
        session.flush()

        state = validated.molding_machine_state

        machine_state = MoldingMachineState(
            inspection_id=inspection.id,
            **state.model_dump(exclude_none=True)
        )
        session.add(machine_state)

        for od_name, od in validated.object_detections.items():
            object_detection = ObjectDetection(
                inspection_id=inspection.id,
                name=od_name,
                reject=od.reject,
            )
            session.add(object_detection)
            session.flush()

            defect_fields = {k: getattr(od, k) for k in type(od).model_fields if k.endswith("_defect")}

            for defect_type, defect in defect_fields.items():
                if defect is None:
                    continue

                ps = defect.pixel_severity if defect.pixel_severity is not None else None

                defect_row = Defect(
                    object_detection_id=object_detection.id,
                    defect_type=defect_type,
                    reject=defect.reject,
                )
                session.add(defect_row)
                session.flush()

                pixel_severity = PixelSeverity(
                    defect_id=defect_row.id,
                    value=ps.value,
                    reject=ps.reject,
                    min_value=ps.min_value,
                    max_value=ps.max_value,
                    threshold=ps.threshold,
                )
                session.add(pixel_severity)

        session.commit()
        session.refresh(inspection)
        return inspection

    except Exception:
        session.rollback()
        raise

    finally:
        if created_session:
            session.close()


def ingest_from_url(url: Optional[str] = None, db_session=None) -> List[ProductInspection]:
    url = url or DEFAULT_URL

    if url.startswith("file://") or os.path.isfile(url):
        path = url[len("file://"):] if url.startswith("file://") else url
        with open(path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
    else:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json, text/plain, */*",
                "Referer": "/",
            }
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            payload = resp.json()
        except Exception:
            req = Request(url, headers={"User-Agent": "ingest-script/1.0"})
            with urlopen(req) as resp:
                payload = json.load(resp)

    saved: List[ProductInspection] = []

    if isinstance(payload, list):
        for item in payload:
            try:
                saved.append(ingest_one(item, db_session=db_session))
            except Exception as exc:
                raise RuntimeError(f"Failed to ingest item: {item}") from exc
    elif isinstance(payload, dict):
        saved.append(ingest_one(payload, db_session=db_session))
    else:
        raise ValueError("Unsupported payload type")

    return saved


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Dataset URL (overrides DATASET_URL)")
    args = parser.parse_args()

    db_gen = get_db()
    db_session = next(db_gen)

    try:
        results = ingest_from_url(args.url, db_session=db_session)
    finally:
        db_session.close()