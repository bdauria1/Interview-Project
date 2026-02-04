from fastapi import FastAPI
from app.endpoints.inspections import router as inspections
from app.endpoints.analytics import router as analytics

app = FastAPI(title="Krevera Take-Home")

app.include_router(inspections)
app.include_router(analytics)