from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.traffic import TrafficData
from app.services.traffic_service import get_traffic


router = APIRouter(
    prefix="/traffic",
    tags=["Traffic"]
)


@router.get("/test")
async def test_traffic():
    try:
        latitude = 19.076
        longitude = 72.8777

        traffic = await get_traffic(
            latitude,
            longitude
        )

        return {
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "traffic": traffic
        }

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Traffic service error: {str(e)}"
        )


@router.post("/collect")
async def collect_traffic(
    db: Session = Depends(get_db)
):
    latitude = 19.076
    longitude = 72.8777

    try:
        traffic = await get_traffic(
            latitude,
            longitude
        )

        record = TrafficData(
            latitude=latitude,
            longitude=longitude,
            timestamp=datetime.now().astimezone(),

            current_speed=traffic[
                "current_speed"
            ],

            free_flow_speed=traffic[
                "free_flow_speed"
            ],

            current_travel_time=traffic[
                "current_travel_time"
            ],

            free_flow_travel_time=traffic[
                "free_flow_travel_time"
            ],

            confidence=traffic[
                "confidence"
            ],

            road_closure=traffic[
                "road_closure"
            ]
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "message": "Traffic data collected successfully",
            "record_id": record.id,
            "traffic": traffic
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=502,
            detail=f"Traffic collection failed: {str(e)}"
        )

@router.post("/collect/{location_id}")
async def collect_traffic_for_location(
    location_id: int,
    db: Session = Depends(get_db)
):
    from app.models.location import Location

    location = (
        db.query(Location)
        .filter(Location.id == location_id)
        .first()
    )

    if not location:
        raise HTTPException(
            status_code=404,
            detail="Location not found"
        )

    try:
        traffic = await get_traffic(
            location.latitude,
            location.longitude
        )

        road_distance = traffic.get(
            "distance_to_road_meters"
        )

        if (
            road_distance is None
            or road_distance > 100
        ):
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Location is too far from a TomTom road segment",
                    "location_id": location.id,
                    "location_name": location.name,
                    "distance_to_road_meters": road_distance,
                    "maximum_allowed_meters": 100
                }
            )

        record = TrafficData(
            location_id=location.id,
            latitude=location.latitude,
            longitude=location.longitude,
            timestamp=datetime.now().astimezone(),
            current_speed=traffic["current_speed"],
            free_flow_speed=traffic["free_flow_speed"],
            current_travel_time=traffic[
                "current_travel_time"
            ],
            free_flow_travel_time=traffic[
                "free_flow_travel_time"
            ],
            confidence=traffic["confidence"],
            road_closure=traffic["road_closure"]
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "message": "Traffic data collected successfully",
            "location": {
                "id": location.id,
                "name": location.name,
                "latitude": location.latitude,
                "longitude": location.longitude
            },
            "record_id": record.id,
            "traffic": traffic
        }

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=502,
            detail=f"Traffic collection failed: {str(e)}"
        )


@router.post("/collect-batch")
async def collect_traffic_batch(
    db: Session = Depends(get_db)
):
    from app.models.location import Location

    locations = (
        db.query(Location)
        .filter(Location.is_active == True)
        .order_by(Location.id)
        .limit(20)
        .all()
    )

    if not locations:
        raise HTTPException(
            status_code=404,
            detail="No active locations found"
        )

    results = []
    successful = 0
    failed = 0

    for location in locations:
        try:
            traffic = await get_traffic(
                location.latitude,
                location.longitude
            )

            road_distance = traffic.get(
                "distance_to_road_meters"
            )

            if (
                road_distance is None
                or road_distance > 100
            ):
                failed += 1

                results.append({
                    "location_id": location.id,
                    "location_name": location.name,
                    "status": "rejected",
                    "reason": (
                        "Too far from TomTom "
                        "road segment"
                    ),
                    "distance_to_road_meters":
                        road_distance
                })

                continue

            record = TrafficData(
                location_id=location.id,
                latitude=location.latitude,
                longitude=location.longitude,
                timestamp=datetime.now().astimezone(),
                current_speed=traffic[
                    "current_speed"
                ],
                free_flow_speed=traffic[
                    "free_flow_speed"
                ],
                current_travel_time=traffic[
                    "current_travel_time"
                ],
                free_flow_travel_time=traffic[
                    "free_flow_travel_time"
                ],
                confidence=traffic[
                    "confidence"
                ],
                road_closure=traffic[
                    "road_closure"
                ]
            )

            db.add(record)
            db.flush()
            successful += 1

            results.append({
                "location_id": location.id,
                "location_name": location.name,
                "status": "collected",
                "record_id": record.id,
                "distance_to_road_meters":
                    road_distance,
                "current_speed":
                    traffic["current_speed"],
                "free_flow_speed":
                    traffic["free_flow_speed"],
                "congestion_percentage":
                    traffic[
                        "congestion_percentage"
                    ],
                "congestion_level":
                    traffic[
                        "congestion_level"
                    ]
            })

        except Exception as e:
            failed += 1

            results.append({
                "location_id": location.id,
                "location_name": location.name,
                "status": "failed",
                "error": str(e)
            })

    db.commit()

    return {
        "total_locations": len(locations),
        "successful": successful,
        "failed": failed,
        "results": results
    }