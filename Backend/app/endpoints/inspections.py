import math
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.repositories.inspection_repository import InspectionRepository

router = APIRouter(prefix="/api/inspections", tags=["inspections"])

@router.get("")
def list_inspections(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    machine_id: Optional[str] = None,
    has_defects: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    repo = InspectionRepository(db)
    inspections, total = repo.get_paginated_inspections(
        page=page, 
        page_size=page_size, 
        machine_id=machine_id, 
        has_defects=has_defects
    )

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": math.ceil(total / page_size) if total else 0,
        "inspections": inspections,
    }

@router.get("/{inspection_id}")
def get_inspection(inspection_id: int, db: Session = Depends(get_db)):
    repo = InspectionRepository(db)
    inspection = repo.get_by_id(inspection_id)

    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")

    return inspection

@router.get("/machine/{machine_id}/count")
def get_machine_inspection_count(machine_id: str, db: Session = Depends(get_db)):
    repo = InspectionRepository(db)
    count = repo.get_count_by_machine(machine_id)
    
    return {"machine_id": machine_id, "inspection_count": count}