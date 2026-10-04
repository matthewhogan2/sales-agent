import json
import urllib.parse
import urllib.request
from typing import List

from app import config

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
USER_AGENT = "sales-agent/0.1 (+https://github.com/matthewhogan2/sales-agent)"


def build_overpass_query(lat: float, lon: float, radius: int,
                         crafts: list[str], shops: list[str]) -> str:
    clauses = []

    if crafts:
        clauses.append(
            f'nwr(around:{radius},{lat},{lon})["name"]["craft"~"{"|".join(crafts)}"];'
        )
    if shops:
        clauses.append(
            f'nwr(around:{radius},{lat},{lon})["name"]["shop"~"{"|".join(shops)}"];'
        )

    return f"""
[out:json][timeout:30];
(
  {chr(10).join(clauses)}
);
out center tags;
"""


def classify_industry(tags: dict) -> str:
    for key in ("craft", "shop", "office"):
        value = tags.get(key, "").lower()
        if value:
            return value.replace("_", " ").title()
    return "Unknown"


def get_coordinates(element: dict):
    if "lat" in element and "lon" in element:
        return element["lat"], element["lon"]

    center = element.get("center")
    if center:
        return center.get("lat"), center.get("lon")

    return None, None


def discover_prospects() -> List[dict]:
    """
    Discover businesses from OpenStreetMap matching the categories
    and area configured in .env.
    """
    if config.DISCOVERY_LAT is None or config.DISCOVERY_LON is None:
        raise ValueError("Set DISCOVERY_LAT and DISCOVERY_LON in .env")

    if not config.DISCOVERY_CRAFTS and not config.DISCOVERY_SHOPS:
        raise ValueError("Set DISCOVERY_CRAFTS and/or DISCOVERY_SHOPS in .env")

    query = build_overpass_query(
        float(config.DISCOVERY_LAT),
        float(config.DISCOVERY_LON),
        config.DISCOVERY_RADIUS_M,
        config.DISCOVERY_CRAFTS,
        config.DISCOVERY_SHOPS,
    )

    request = urllib.request.Request(
        OVERPASS_URL,
        data=urllib.parse.urlencode({"data": query}).encode("utf-8"),
        headers={"User-Agent": USER_AGENT},
    )

    with urllib.request.urlopen(request, timeout=90) as response:
        data = json.loads(response.read().decode("utf-8"))

    prospects = []

    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = tags.get("name")
        if not name:
            continue

        latitude, longitude = get_coordinates(element)

        prospects.append({
            "name": name,
            "industry": classify_industry(tags),
            "address": tags.get("addr:full"),
            "website": tags.get("website"),
            "phone": tags.get("phone"),
            "email": tags.get("email"),
            "latitude": str(latitude) if latitude else None,
            "longitude": str(longitude) if longitude else None,
            "source": "openstreetmap_overpass",
        })

    return prospects
