# from sqlalchemy import Column, String, Float, Boolean
# from sqlalchemy.dialects.postgresql import UUID
# from db import Base
# from pydantic import BaseModel
# from typing import Optional
# from enum import Enum
# from datetime import datetime
# import uuid

# # ── SQLAlchemy ORM Model (Supabase/PostgreSQL table) ────────────────────────
# class Driver(Base):
#     __tablename__ = "drivers"
#     id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name         = Column(String, nullable=False)
#     phone        = Column(String, nullable=False)
#     vehicle_type = Column(String, nullable=True)
#     current_lat  = Column(Float, nullable=True)
#     current_lng  = Column(Float, nullable=True)
#     is_available = Column(Boolean, default=True)

# # ── Pydantic Schemas (API request / response shapes) ────────────────────────
# class DriverStatus(str, Enum):
#     AVAILABLE = "available"
#     ON_TRIP   = "on_trip"
#     OFFLINE   = "offline"

# class Location(BaseModel):
#     lat: float
#     lng: float

# class DriverSchema(BaseModel):
#     driver_id: str
#     name: str
#     phone: str
#     vehicle_type: str
#     status: DriverStatus = DriverStatus.AVAILABLE
#     current_location: Location
#     rating: float = 5.0
#     registered_at: str = datetime.utcnow().isoformat()

# class RegisterDriverRequest(BaseModel):
#     name: str
#     phone: str
#     vehicle_type: str
#     current_location: Location

# class UpdateLocationRequest(BaseModel):
#     driver_id: str
#     current_location: Location

# class AssignDriverRequest(BaseModel):
#     order_id: str
#     pickup_location: Location
#     dropoff_location: Location
#     vehicle_type: Optional[str] = None

# class AssignmentResult(BaseModel):
#     order_id: str
#     driver_id: str
#     driver_name: str
#     driver_phone: str
#     pickup_location: Location
#     dropoff_location: Location
#     straight_line_km: float
#     driving_distance_km: Optional[float]
#     estimated_duration_mins: Optional[float]
#     distance_to_pickup_km: float
#     assigned_at: str


from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from db import Base
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime
import uuid

# ── SQLAlchemy ORM ───────────────────────────────────────────────────────────
class Driver(Base):
    __tablename__ = "drivers"
    id            = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name          = Column(String, nullable=False)
    phone         = Column(String, nullable=False)
    vehicle_type  = Column(String, nullable=True)
    current_lat   = Column(Float, nullable=True)
    current_lng   = Column(Float, nullable=True)
    is_available  = Column(Boolean, default=True)
    rating        = Column(Float, default=5.0)       # ← average rating
    total_ratings = Column(Integer, default=0)       # ← number of ratings
    total_trips   = Column(Integer, default=0)       # ← completed trips
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

# ── Pydantic Schemas ─────────────────────────────────────────────────────────
class DriverStatus(str, Enum):
    AVAILABLE = "available"
    ON_TRIP   = "on_trip"
    OFFLINE   = "offline"

class Location(BaseModel):
    lat: float
    lng: float

class DriverSchema(BaseModel):
    driver_id: str
    name: str
    phone: str
    vehicle_type: str
    status: DriverStatus = DriverStatus.AVAILABLE
    current_location: Location
    rating: float = 5.0
    total_trips: int = 0
    registered_at: str = datetime.utcnow().isoformat()

class RegisterDriverRequest(BaseModel):
    name: str
    phone: str
    vehicle_type: str
    current_location: Location

class UpdateLocationRequest(BaseModel):
    driver_id: str
    current_location: Location

class AssignDriverRequest(BaseModel):
    order_id: str
    pickup_location: Location
    dropoff_location: Location
    vehicle_type: Optional[str] = None

class AssignmentResult(BaseModel):
    order_id: str
    driver_id: str
    driver_name: str
    driver_phone: str
    pickup_location: Location
    dropoff_location: Location
    straight_line_km: float
    driving_distance_km: Optional[float]
    estimated_duration_mins: Optional[float]
    distance_to_pickup_km: float
    surge_multiplier: float = 1.0
    final_price: float = 50.0
    assigned_at: str