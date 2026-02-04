from sqlalchemy import Column, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class PixelSeverity(Base):
    __tablename__ = "pixel_severities"

    id = Column(Integer, primary_key=True)
    defect_id = Column(Integer, ForeignKey("defects.id"), unique=True, nullable=False)
    reject = Column(Boolean, nullable=False)
    value = Column(Float, nullable=False)
    min_value = Column(Float)
    max_value = Column(Float)
    threshold = Column(Float)
    defect = relationship("Defect", back_populates="pixel_severity")
