from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from .defect import DefectBase

class ObjectDetectionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    reject: bool
    discoloration_defect: Optional[DefectBase] = None
    discoloration_patch_defect: Optional[DefectBase] = None
    flash_defect: Optional[DefectBase] = None
    short_defect: Optional[DefectBase] = None
    contamination_defect: Optional[DefectBase] = None
    splay_defect: Optional[DefectBase] = None
    burn_mark_defect: Optional[DefectBase] = None
    jetting_defect: Optional[DefectBase] = None
    flow_mark_defect: Optional[DefectBase] = None
    sink_mark_defect: Optional[DefectBase] = None
    knit_line_defect: Optional[DefectBase] = None
    void_defect: Optional[DefectBase] = None
    ejector_pin_mark_defect: Optional[DefectBase] = None
    label_detection: Optional[Dict[str, Any]] = None