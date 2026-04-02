from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.route_optimizer import optimize_multi_stop_route
from services.location_history import location_history
from services.surge_service import surge_calculator
from models.driver import Location

router = APIRouter(prefix="/routes", tags=["Routes"])

class MultiStopRequest(BaseModel):
    driver_location: Location
    stops: list[Location]

class SurgeRequest(BaseModel):
    lat: float
    lng: float
    available_drivers: int

@router.post("/optimize")
def optimize_route(req: MultiStopRequest):
    if len(req.stops) == 0:
        raise HTTPException(400, "At least one stop required")
    if len(req.stops) > 10:
        raise HTTPException(400, "Max 10 stops supported")

    route, total_distance = optimize_multi_stop_route(
        req.driver_location, req.stops
    )
    return {
        "optimized_route":   [{"lat": s.lat, "lng": s.lng} for s in route],
        "total_distance_km": total_distance,
        "total_stops":       len(route),
    }

@router.get("/location-history/{driver_id}")
def get_location_history(driver_id: str, last_n: int = 10):
    history = location_history.get_history(driver_id, last_n)
    return {
        "driver_id": driver_id,
        "history":   history,
        "count":     len(history),
    }

@router.post("/surge")
def get_surge(req: SurgeRequest):
    multiplier = surge_calculator.get_surge_multiplier(
        req.lat, req.lng, req.available_drivers
    )
    stats = surge_calculator.get_zone_stats(req.lat, req.lng)
    return {
        "surge_multiplier":  multiplier,
        "is_surge":          multiplier > 1.0,
        "zone_stats":        stats,
    }