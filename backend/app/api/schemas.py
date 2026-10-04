from pydantic import BaseModel
from typing import Optional


class CompanyCreate(BaseModel):
    name: str
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    industry: Optional[str] = None
    source: Optional[str] = None


class LeadCreate(BaseModel):
    company_id: int
    status: str = "new"
    fit_score: Optional[int] = None
    fit_reason: Optional[str] = None
    product: Optional[str] = None
    outreach_angle: Optional[str] = None
    distance_km: Optional[str] = None
