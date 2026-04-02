from pydantic import BaseModel

class LocationUpdate(BaseModel):
    driver_id: str
    lat: float
    lng: float