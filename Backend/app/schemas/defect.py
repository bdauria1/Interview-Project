from pydantic import BaseModel, ConfigDict
from .pixel_severity import PixelSeverity

class DefectBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    reject: bool
    pixel_severity: PixelSeverity
