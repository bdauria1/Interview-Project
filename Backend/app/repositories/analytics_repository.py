from sqlalchemy.orm import Session
from sqlalchemy import select, func, case, and_
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.models.product_inspection import ProductInspection
from app.models.molding_machine_state import MoldingMachineState
from app.models.object_detection import ObjectDetection
from app.models.defect import Defect

class AnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def _get_has_defects_subquery(self):
        return (
            select(func.count(Defect.id))
            .select_from(ObjectDetection)
            .join(Defect)
            .where(ObjectDetection.inspection_id == ProductInspection.id)
            .scalar_subquery()
        )

    def get_defect_trends(
        self, 
        grouping: str, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None, 
        machine_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query = (
            select(
                func.date_trunc(grouping, ProductInspection.timestamp).label("period"),
                func.count(func.distinct(ProductInspection.id)).label("total_count"),
                func.count(func.distinct(Defect.id)).label("defect_count"),
            )
            .select_from(ProductInspection)
            .join(ObjectDetection, ProductInspection.id == ObjectDetection.inspection_id, isouter=True)
            .join(Defect, ObjectDetection.id == Defect.object_detection_id, isouter=True)
        )
        
        conditions = []
        if start_date: conditions.append(ProductInspection.timestamp >= start_date)
        if end_date: conditions.append(ProductInspection.timestamp <= end_date)
        if machine_id: conditions.append(ProductInspection.molding_machine_id == machine_id)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.group_by("period").order_by("period")
        result = self.db.execute(query).all()
        
        return [
            {
                "timestamp": row.period.isoformat(),
                "total_count": row.total_count,
                "defect_count": row.defect_count,
                "defect_rate": round((row.defect_count / row.total_count * 100), 2) if row.total_count > 0 else 0.0,
            } for row in result
        ]

    def get_machine_performance(
        self, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        query = (
            select(
                ProductInspection.molding_machine_id,
                func.avg(MoldingMachineState.CycleTime).label("avg_cycle"),
                func.avg(MoldingMachineState.InjPeakPressure).label("avg_pressure"),
                func.avg((
                    MoldingMachineState.Barrel1 + MoldingMachineState.Barrel2 + 
                    MoldingMachineState.Barrel3 + MoldingMachineState.Barrel4 + 
                    MoldingMachineState.Barrel5 + MoldingMachineState.Barrel6
                ) / 6.0).label("avg_temp"),
                func.count(func.distinct(ProductInspection.id)).label("total"),
                func.count(func.distinct(Defect.id)).label("defects"),
            )
            .select_from(ProductInspection)
            .join(MoldingMachineState, ProductInspection.id == MoldingMachineState.inspection_id, isouter=True)
            .join(ObjectDetection, ProductInspection.id == ObjectDetection.inspection_id, isouter=True)
            .join(Defect, ObjectDetection.id == Defect.object_detection_id, isouter=True)
        )
        
        conditions = []
        if start_date: conditions.append(ProductInspection.timestamp >= start_date)
        if end_date: conditions.append(ProductInspection.timestamp <= end_date)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.group_by(ProductInspection.molding_machine_id).order_by(ProductInspection.molding_machine_id)
        result = self.db.execute(query).all()
        
        return [
            {
                "machine_id": row.molding_machine_id,
                "avg_cycle_time": round(row.avg_cycle, 2) if row.avg_cycle else None,
                "avg_injection_pressure": round(row.avg_pressure, 2) if row.avg_pressure else None,
                "avg_barrel_temp": round(row.avg_temp, 2) if row.avg_temp else None,
                "total_inspections": row.total,
                "defect_count": row.defects,
                "defect_rate": round((row.defects / row.total * 100), 2) if row.total > 0 else 0.0,
            } for row in result
        ]

    def get_defect_distribution(
        self, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None, 
        machine_id: Optional[str] = None
    ) -> Dict[str, Any]:
        query = (
            select(Defect.defect_type, func.count(Defect.id).label("count"))
            .join(ObjectDetection, Defect.object_detection_id == ObjectDetection.id)
            .join(ProductInspection, ObjectDetection.inspection_id == ProductInspection.id)
        )
        
        conditions = []
        if start_date: conditions.append(ProductInspection.timestamp >= start_date)
        if end_date: conditions.append(ProductInspection.timestamp <= end_date)
        if machine_id: conditions.append(ProductInspection.molding_machine_id == machine_id)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.group_by(Defect.defect_type).order_by(func.count(Defect.id).desc())
        rows = self.db.execute(query).all()
        
        total_defects = sum(row.count for row in rows)
        distribution = [
            {
                "defect_type": row.defect_type,
                "count": row.count,
                "percentage": round((row.count / total_defects * 100), 2) if total_defects > 0 else 0.0
            } for row in rows
        ]
        return {"distribution": distribution, "total_defects": total_defects}

    def get_summary_metrics(
        self, 
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        query = (
            select(
                func.count(func.distinct(ProductInspection.id)).label("total_inspections"),
                func.count(func.distinct(Defect.id)).label("total_defects"),
                func.count(func.distinct(ProductInspection.molding_machine_id)).label("total_machines"),
                func.min(ProductInspection.timestamp).label("date_start"),
                func.max(ProductInspection.timestamp).label("date_end"),
            )
            .select_from(ProductInspection)
            .join(ObjectDetection, ProductInspection.id == ObjectDetection.inspection_id, isouter=True)
            .join(Defect, ObjectDetection.id == Defect.object_detection_id, isouter=True)
        )
        
        conditions = []
        if start_date: conditions.append(ProductInspection.timestamp >= start_date)
        if end_date: conditions.append(ProductInspection.timestamp <= end_date)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        row = self.db.execute(query).one()
        total_inspections = row.total_inspections or 0
        total_defects = row.total_defects or 0
        
        return {
            "total_inspections": total_inspections,
            "total_defects": total_defects,
            "defect_rate": round((total_defects / total_inspections * 100), 2) if total_inspections > 0 else 0.0,
            "total_machines": row.total_machines or 0,
            "date_start": row.date_start,
            "date_end": row.date_end,
        }