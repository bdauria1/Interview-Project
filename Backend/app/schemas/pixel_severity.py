from pydantic import BaseModel, ConfigDict

class PixelSeverity(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    reject: bool
    value: float
    min_value: float
    max_value: float
    threshold: float

class LabelDetection(BaseModel):
    # In the dataset label_detection is an empty object so we just pass
    model_config = ConfigDict(from_attributes=True)
    pass