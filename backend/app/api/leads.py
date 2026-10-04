from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.lead import Lead
from app.api.schemas import LeadCreate

router = APIRouter(prefix="/leads", tags=["leads"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).all()


@router.post("/")
def create_lead(
    lead_data: LeadCreate,
    db: Session = Depends(get_db)
):
    lead = Lead(**lead_data.model_dump())

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return lead
