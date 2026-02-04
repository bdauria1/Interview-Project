from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ObjectDetection(Base):
    __tablename__ = "object_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("product_inspections.id"), nullable=False)
    name = Column(String, nullable=False)
    reject = Column(Boolean, nullable=False)
    inspection = relationship("ProductInspection", back_populates="object_detections")
    defects = relationship("Defect", back_populates="object_detection", cascade="all, delete-orphan")