from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Defect(Base):
    __tablename__ = "defects"

    id = Column(Integer, primary_key=True)
    object_detection_id = Column(Integer, ForeignKey("object_detections.id"), nullable=False)
    defect_type = Column(String, nullable=False)
    reject = Column(Boolean, nullable=False)
    object_detection = relationship("ObjectDetection", back_populates="defects")
    pixel_severity = relationship("PixelSeverity", back_populates="defect", uselist=False, cascade="all, delete-orphan")