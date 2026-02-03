from pydantic import BaseModel, ConfigDict
from typing import Dict, Any
from .object_detection import ObjectDetectionBase
from sqlalchemy import DateTime

class ProjectInspectionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    version: str
    timestamp: DateTime
    molding_machine_id: str
    molding_machine_state: Dict[str, Any]
    object_detections: Dict[str, ObjectDetectionBase]