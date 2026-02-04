from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ProductInspection(Base):
    __tablename__ = "product_inspections"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    molding_machine_id = Column(String, nullable=False)
    molding_machine_state = relationship("MoldingMachineState", back_populates="inspection", uselist=False, cascade="all, delete-orphan")
    object_detections = relationship("ObjectDetection", back_populates="inspection", cascade="all, delete-orphan")