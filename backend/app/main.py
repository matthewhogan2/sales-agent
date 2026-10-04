from fastapi import FastAPI

from app.database import Base, engine
from app.models.company import Company
from app.models.lead import Lead
from app.api.companies import router as companies_router
from app.api.leads import router as leads_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sales Agent")

app.include_router(companies_router)
app.include_router(leads_router)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Sales Agent"
    }
