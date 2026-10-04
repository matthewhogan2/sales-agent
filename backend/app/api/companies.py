from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.company import Company
from app.api.schemas import CompanyCreate

router = APIRouter(prefix="/companies", tags=["companies"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    return db.query(Company).all()


@router.post("/")
def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db)
):
    company = Company(**company_data.model_dump())

    db.add(company)
    db.commit()
    db.refresh(company)

    return company
