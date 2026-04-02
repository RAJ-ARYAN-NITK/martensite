from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rating_service import rate_driver, get_top_drivers

router = APIRouter(prefix="/ratings", tags=["Ratings"])

class RatingRequest(BaseModel):
    driver_id: str
    rating: float
    order_id: str

@router.post("/")
def submit_rating(req: RatingRequest):
    try:
        driver = rate_driver(req.driver_id, req.rating)
    except ValueError as e:
        raise HTTPException(400, str(e))
    if not driver:
        raise HTTPException(404, "Driver not found")
    return {
        "message": "Rating submitted",
        "driver_id": str(driver.id),
        "new_rating": driver.rating,
        "total_ratings": driver.total_ratings,
    }

@router.get("/top-drivers")
def top_drivers(limit: int = 10):
    drivers = get_top_drivers(limit)
    return {
        "count": len(drivers),
        "drivers": [
            {
                "id": str(d.id),
                "name": d.name,
                "rating": d.rating,
                "total_trips": d.total_trips,
                "vehicle_type": d.vehicle_type,
            }
            for d in drivers
        ]
    }