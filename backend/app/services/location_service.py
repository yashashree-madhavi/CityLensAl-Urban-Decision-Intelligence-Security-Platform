import httpx

from sqlalchemy.orm import Session

from app.models.location import Location


OVERPASS_URL = "https://overpass-api.de/api/interpreter"


MUMBAI_BBOX = "18.85,72.75,19.30,73.00"


OVERPASS_QUERY = f"""
[out:json][timeout:60];

(
  nwr({MUMBAI_BBOX})["place"="neighbourhood"];
  nwr({MUMBAI_BBOX})["place"="suburb"];
  nwr({MUMBAI_BBOX})["place"="quarter"];
);

out center;
"""


async def sync_mumbai_locations(db: Session):

    async with httpx.AsyncClient(
        timeout=60.0,
        headers={
            "User-Agent": "CityLensAI/1.0 (Urban Decision Intelligence Project)",
            "Accept": "application/json",
        }
    ) as client:

        response = await client.post(
            OVERPASS_URL,
            data=OVERPASS_QUERY
        )

        response.raise_for_status()

        data = response.json()

    locations = data.get("elements", [])

    inserted = 0
    skipped = 0

    for item in locations:

        tags = item.get("tags", {})

        name = (
            tags.get("name:en")
            or tags.get("name")
        )

        if not name:
            skipped += 1
            continue

        # Nodes have lat/lon directly.
        # Ways/relations have coordinates inside "center".
        latitude = item.get("lat")
        longitude = item.get("lon")

        if latitude is None or longitude is None:
            center = item.get("center", {})

            latitude = center.get("lat")
            longitude = center.get("lon")

        if latitude is None or longitude is None:
            skipped += 1
            continue

        # Avoid duplicate locations with the same name.
        existing = (
            db.query(Location)
            .filter(Location.name == name)
            .first()
        )

        if existing:
            skipped += 1
            continue

        location = Location(
            name=name,
            latitude=latitude,
            longitude=longitude,
            is_active=True
        )

        db.add(location)
        inserted += 1

    db.commit()

    return {
        "source": "OpenStreetMap Overpass API",
        "total_found": len(locations),
        "inserted": inserted,
        "skipped": skipped
    }