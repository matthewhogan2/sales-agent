from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    website = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    industry = Column(String)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
