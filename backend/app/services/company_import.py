import math
import re

from app.database import SessionLocal
from app.models.company import Company

SUFFIXES = r"\b(ltd|limited|teo|inc|co|company|and sons|& sons)\b"
SAME_PLACE_KM = 5.0


def normalise_name(name: str | None) -> str:
    if not name:
        return ""
    n = name.lower().replace("'", "").replace("’", "")
    n = re.sub(SUFFIXES, " ", n)
    n = re.sub(r"[^\w\s]", " ", n)
    return " ".join(n.split())


def normalise_phone(phone: str | None) -> str:
    if not phone:
        return ""
    digits = re.sub(r"\D", "", phone)
    return digits[-9:]  # ignores +353 / 0 prefix differences


def normalise_website(url: str | None) -> str:
    if not url:
        return ""
    u = url.lower().strip()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    return u.rstrip("/")


def distance_km(lat1, lon1, lat2, lon2) -> float | None:
    try:
        lat1, lon1, lat2, lon2 = map(float, (lat1, lon1, lat2, lon2))
    except (TypeError, ValueError):
        return None
    r = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dlon / 2) ** 2)
    return 2 * r * math.asin(math.sqrt(a))


def is_duplicate(candidate: dict, known: list[dict]) -> bool:
    name = normalise_name(candidate.get("name"))
    phone = normalise_phone(candidate.get("phone"))
    site = normalise_website(candidate.get("website"))

    for k in known:
        if phone and phone == k["phone"]:
            return True
        if site and site == k["site"]:
            return True
        if name and name == k["name"]:
            d = distance_km(candidate.get("latitude"), candidate.get("longitude"),
                            k["lat"], k["lon"])
            if d is None or d <= SAME_PLACE_KM:
                return True
    return False


def _key(name, phone, website, lat, lon) -> dict:
    return {
        "name": normalise_name(name),
        "phone": normalise_phone(phone),
        "site": normalise_website(website),
        "lat": lat,
        "lon": lon,
    }


def import_prospects(prospects: list[dict]) -> int:
    db = SessionLocal()
    imported = 0

    try:
        known = [
            _key(c.name, c.phone, c.website, c.latitude, c.longitude)
            for c in db.query(Company).all()
        ]

        for prospect in prospects:
            if is_duplicate(prospect, known):
                continue

            db.add(Company(**prospect))
            known.append(_key(prospect.get("name"), prospect.get("phone"),
                              prospect.get("website"), prospect.get("latitude"),
                              prospect.get("longitude")))
            imported += 1

        db.commit()
        return imported

    finally:
        db.close()
