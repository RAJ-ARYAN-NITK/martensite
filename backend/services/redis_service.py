import redis
import json
import os

r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

def update_driver_location(driver_id: str, lat: float, lng: float):
    r.setex(f"driver:{driver_id}:location", 30, json.dumps({
        "lat": lat,
        "lng": lng
    }))

def get_driver_location(driver_id: str):
    data = r.get(f"driver:{driver_id}:location")
    return json.loads(data) if data else None

def set_driver_available(driver_id: str, available: bool):
    r.setex(f"driver:{driver_id}:status", 30,
            "available" if available else "busy")

def get_available_drivers(driver_ids: list):
    available = []
    for driver_id in driver_ids:
        status = r.get(f"driver:{driver_id}:status")
        if status and status.decode() == "available":
            available.append(driver_id)
    return available