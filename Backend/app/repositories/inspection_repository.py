from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from typing import Optional, List, Tuple
from app.models.product_inspection import ProductInspection
from app.models.object_detection import ObjectDetection

class InspectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_paginated_inspections(
        self, 
        page: int, 
        page_size: int, 
        machine_id: Optional[str] = None, 
        has_defects: Optional[bool] = None
    ) -> Tuple[List[ProductInspection], int]:
        query = select(ProductInspection).options(
            selectinload(ProductInspection.molding_machine_state),
            selectinload(ProductInspection.object_detections)
            .selectinload(ObjectDetection.defects),
        )

        if machine_id:
            query = query.where(ProductInspection.molding_machine_id == machine_id)

        if has_defects is True:
            query = (
                query.join(ProductInspection.object_detections)
                .join(ObjectDetection.defects)
                .distinct()
            )

        count_query = select(func.count()).select_from(query.subquery())
        total = self.db.execute(count_query).scalar() or 0

        offset = (page - 1) * page_size
        query = (
            query.order_by(ProductInspection.timestamp.desc())
            .offset(offset)
            .limit(page_size)
        )
        
        results = self.db.execute(query).scalars().all()
        return list(results), total

    def get_by_id(self, inspection_id: int) -> Optional[ProductInspection]:
        query = select(ProductInspection).options(
            selectinload(ProductInspection.molding_machine_state),
            selectinload(ProductInspection.object_detections)
            .selectinload(ObjectDetection.defects),
        ).where(ProductInspection.id == inspection_id)
        
        return self.db.execute(query).scalar_one_or_none()

    def get_count_by_machine(self, machine_id: str) -> int:
        query = select(func.count()).where(ProductInspection.molding_machine_id == machine_id)
        return self.db.execute(query).scalar() or 0