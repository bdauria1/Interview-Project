from pydantic import BaseModel, ConfigDict
from typing import Dict, Any
from .object_detection import ObjectDetectionBase
from .molding_machine_state import MoldingMachineStateBase
from datetime import datetime

class ProjectInspectionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    version: str
    timestamp: datetime
    molding_machine_id: str
    molding_machine_state: MoldingMachineStateBase
    object_detections: Dict[str, ObjectDetectionBase]