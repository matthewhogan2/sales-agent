import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _csv(name: str) -> list[str]:
    return [item.strip() for item in os.getenv(name, "").split(",") if item.strip()]


DATABASE_URL = os.environ["DATABASE_URL"]

DISCOVERY_LAT = os.getenv("DISCOVERY_LAT")
DISCOVERY_LON = os.getenv("DISCOVERY_LON")
DISCOVERY_RADIUS_M = int(os.getenv("DISCOVERY_RADIUS_M", "5000"))
DISCOVERY_CRAFTS = _csv("DISCOVERY_CRAFTS")
DISCOVERY_SHOPS = _csv("DISCOVERY_SHOPS")
