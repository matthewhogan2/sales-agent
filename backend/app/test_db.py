from app.database import SessionLocal
from app.models.company import Company

db = SessionLocal()

company = Company(
    name="Test Roofing Ltd",
    website="https://example.com",
    email="test@example.com",
    address="1 Example Street",
    industry="Roofing",
    source="test"
)

db.add(company)
db.commit()
db.refresh(company)

print(f"Created company: {company.name}")
print(f"Company ID: {company.id}")

db.close()
