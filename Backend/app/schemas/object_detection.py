from pydantic import BaseModel, ConfigDict
from typing import Dict, Optional
from .defect import DefectBase
from .pixel_severity import LabelDetection

class ObjectDetectionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    reject: bool
    defects: Dict[str, DefectBase]
    label_detection: Optional[LabelDetection] = None