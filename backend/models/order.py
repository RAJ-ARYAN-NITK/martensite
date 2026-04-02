# from sqlalchemy import Column, String, Float, DateTime, Enum
# from sqlalchemy.dialects.postgresql import UUID
# from db import Base
# import uuid
# import datetime
# import enum

# class OrderStatus(str, enum.Enum):
#     PENDING = "pending"
#     ASSIGNED = "assigned"
#     PICKED_UP = "picked_up"
#     IN_TRANSIT = "in_transit"
#     DELIVERED = "delivered"

# class Order(Base):
#     __tablename__ = "orders"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     customer_id = Column(String, nullable=False)
#     pickup_lat = Column(Float, nullable=False)
#     pickup_lng = Column(Float, nullable=False)
#     dropoff_lat = Column(Float, nullable=False)
#     dropoff_lng = Column(Float, nullable=False)
#     status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
#     driver_id = Column(String, nullable=True)
#     created_at = Column(DateTime, default=datetime.datetime.utcnow)

from sqlalchemy import Column, String, Float, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from db import Base
import uuid
import datetime
import enum

class OrderStatus(str, enum.Enum):
    PENDING    = "pending"
    ASSIGNED   = "assigned"
    PICKED_UP  = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED  = "delivered"

class Order(Base):
    __tablename__ = "orders"
    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id      = Column(String, nullable=False)
    pickup_lat       = Column(Float, nullable=False)
    pickup_lng       = Column(Float, nullable=False)
    dropoff_lat      = Column(Float, nullable=False)
    dropoff_lng      = Column(Float, nullable=False)
    status           = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    driver_id        = Column(String, nullable=True)
    surge_multiplier = Column(Float, default=1.0)   # ← surge pricing
    base_price       = Column(Float, default=50.0)  # ← base delivery fee
    final_price      = Column(Float, default=50.0)  # ← after surge
    created_at       = Column(DateTime, default=datetime.datetime.utcnow)