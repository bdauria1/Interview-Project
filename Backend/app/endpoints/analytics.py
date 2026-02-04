from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, Literal
from app.core.database import get_db
from app.repositories.analytics_repository import AnalyticsRepository

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/defect-trends")
async def get_defect_trends(
    grouping: Literal["hour", "day", "week"] = Query("day"),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    machine_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    repo = AnalyticsRepository(db)
    trends = repo.get_defect_trends(grouping, start_date, end_date, machine_id)
    return {"trends": trends, "grouping": grouping}

@router.get("/machine-performance")
async def get_machine_performance(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    repo = AnalyticsRepository(db)
    machines = repo.get_machine_performance(start_date, end_date)
    return {"machines": machines}

@router.get("/defect-distribution")
async def get_defect_distribution(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    machine_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    repo = AnalyticsRepository(db)
    return repo.get_defect_distribution(start_date, end_date, machine_id)

@router.get("/summary")
async def get_summary_metrics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    repo = AnalyticsRepository(db)
    return repo.get_summary_metrics(start_date, end_date)