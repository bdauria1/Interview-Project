from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints.inspections import router as inspections
from app.endpoints.analytics import router as analytics

app = FastAPI(title="Krevera Take-Home")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inspections)
app.include_router(analytics)