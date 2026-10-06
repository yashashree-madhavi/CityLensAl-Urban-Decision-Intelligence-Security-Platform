from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.location_service import sync_mumbai_locations


router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)


@router.post("/sync")
async def sync_locations(
    db: Session = Depends(get_db)
):
    result = await sync_mumbai_locations(db)

    return result