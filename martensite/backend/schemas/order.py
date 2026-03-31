from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class OrderCreate(BaseModel):
    customer_id: str
    pickup_lat: float
    pickup_lng: float
    dropoff_lat: float
    dropoff_lng: float

class OrderResponse(BaseModel):
    id: UUID
    customer_id: str
    pickup_lat: float
    pickup_lng: float
    dropoff_lat: float
    dropoff_lng: float
    status: str
    driver_id: Optional[str]

    class Config:
        from_attributes = True