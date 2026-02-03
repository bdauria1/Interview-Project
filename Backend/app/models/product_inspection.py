from sqlalchemy import Column, Integer, String, JSON
from app.core.database import Base
from sqlalchemy import DateTime

class ProductInspection(Base):
    __tablename__ = "product_inspections"

    id = Column(Integer, primary_key=True)
    version = Column(String)
    timestamp = Column(DateTime)
    molding_machine_id = Column(String, index=True)
    molding_machine_state = Column(JSON)
    object_detections = Column(JSON)