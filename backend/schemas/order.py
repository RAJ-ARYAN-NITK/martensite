# from pydantic import BaseModel
# from uuid import UUID
# from typing import Optional

# class OrderCreate(BaseModel):
#     customer_id: str
#     pickup_lat: float
#     pickup_lng: float
#     dropoff_lat: float
#     dropoff_lng: float

# class OrderResponse(BaseModel):
#     id: UUID
#     customer_id: str
#     pickup_lat: float
#     pickup_lng: float
#     dropoff_lat: float
#     dropoff_lng: float
#     status: str
#     driver_id: Optional[str]

#     class Config:
#         from_attributes = True

# from pydantic import BaseModel
# from uuid import UUID
# from typing import Optional
# from datetime import datetime

# class OrderCreate(BaseModel):
#     customer_id: str
#     pickup_lat: float
#     pickup_lng: float
#     dropoff_lat: float
#     dropoff_lng: float

# class OrderResponse(BaseModel):
#     id: UUID
#     customer_id: str
#     pickup_lat: float
#     pickup_lng: float
#     dropoff_lat: float
#     dropoff_lng: float
#     status: str
#     driver_id: Optional[str]
#     created_at: Optional[datetime]

#     class Config:
#         from_attributes = True

# class OrderStatusUpdate(BaseModel):
#     status: str    

from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

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
    surge_multiplier: Optional[float] = 1.0
    base_price: Optional[float] = 50.0
    final_price: Optional[float] = 50.0
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str