# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from db import get_db
# from models.order import Order
# from schemas.order import OrderCreate, OrderResponse
# from services.kafka_producer import publish_new_order

# router = APIRouter(prefix="/orders", tags=["orders"])

# @router.post("/", response_model=OrderResponse)
# def create_order(order: OrderCreate, db: Session = Depends(get_db)):
#     db_order = Order(**order.model_dump())
#     db.add(db_order)
#     db.commit()
#     db.refresh(db_order)

#     # Publish to Kafka
#     publish_new_order({
#         "order_id": str(db_order.id),
#         "pickup_lat": db_order.pickup_lat,
#         "pickup_lng": db_order.pickup_lng,
#         "dropoff_lat": db_order.dropoff_lat,
#         "dropoff_lng": db_order.dropoff_lng,
#     })

#     return db_order

# @router.get("/{order_id}", response_model=OrderResponse)
# def get_order(order_id: str, db: Session = Depends(get_db)):
#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order

# @router.get("/", response_model=list[OrderResponse])
# def list_orders(db: Session = Depends(get_db)):
#     return db.query(Order).all()

# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from db import get_db
# from models.order import Order
# from schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
# from services.kafka_producer import publish_new_order
# from services.order_service import update_order_status

# router = APIRouter(prefix="/orders", tags=["orders"])


# # ── Create Order ─────────────────────────────────────────────────────────────
# @router.post("/", response_model=OrderResponse)
# def create_order(order: OrderCreate, db: Session = Depends(get_db)):
#     db_order = Order(**order.model_dump())
#     db.add(db_order)
#     db.commit()
#     db.refresh(db_order)

#     # Kafka event → consumer picks this up and auto-assigns a driver
#     publish_new_order({
#         "order_id":    str(db_order.id),
#         "pickup_lat":  db_order.pickup_lat,
#         "pickup_lng":  db_order.pickup_lng,
#         "dropoff_lat": db_order.dropoff_lat,
#         "dropoff_lng": db_order.dropoff_lng,
#     })
#     return db_order


# # ── Get Single Order ─────────────────────────────────────────────────────────
# @router.get("/{order_id}", response_model=OrderResponse)
# def get_order(order_id: str, db: Session = Depends(get_db)):
#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         raise HTTPException(404, "Order not found")
#     return order


# # ── List All Orders ──────────────────────────────────────────────────────────
# @router.get("/", response_model=list[OrderResponse])
# def list_orders(db: Session = Depends(get_db)):
#     return db.query(Order).all()


# # ── Update Order Status ──────────────────────────────────────────────────────
# @router.patch("/{order_id}/status", response_model=OrderResponse)
# def update_status(
#     order_id: str,
#     body: OrderStatusUpdate,
#     db: Session = Depends(get_db)
# ):
#     try:
#         order = update_order_status(order_id, body.status, db)
#     except ValueError as e:
#         raise HTTPException(400, str(e))

#     if not order:
#         raise HTTPException(404, "Order not found")
#     return order


# # ── Get Orders by Status ─────────────────────────────────────────────────────
# @router.get("/status/{status}", response_model=list[OrderResponse])
# def get_orders_by_status(status: str, db: Session = Depends(get_db)):
#     from models.order import OrderStatus
#     try:
#         status_enum = OrderStatus(status)
#     except ValueError:
#         raise HTTPException(400, f"Invalid status: {status}")
#     return db.query(Order).filter(Order.status == status_enum).all()



# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from db import get_db
# from models.order import Order
# from schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
# from services.kafka_producer import publish_new_order
# from services.order_service import update_order_status
# from services.surge_service import surge_calculator
# from services import driver_store

# router = APIRouter(prefix="/orders", tags=["orders"])

# @router.post("/", response_model=OrderResponse)
# def create_order(order: OrderCreate, db: Session = Depends(get_db)):
#     # Calculate surge before creating order
#     available_count = len(driver_store.get_available_drivers())
#     surge = surge_calculator.get_surge_multiplier(
#         order.pickup_lat, order.pickup_lng, available_count
#     )
#     base_price  = 50.0
#     final_price = round(base_price * surge, 2)

#     # Record this order in surge calculator sliding window
#     surge_calculator.record_order(order.pickup_lat, order.pickup_lng)

#     db_order = Order(
#         **order.model_dump(),
#         surge_multiplier=surge,
#         base_price=base_price,
#         final_price=final_price
#     )
#     db.add(db_order)
#     db.commit()
#     db.refresh(db_order)

#     publish_new_order({
#         "order_id":    str(db_order.id),
#         "pickup_lat":  db_order.pickup_lat,
#         "pickup_lng":  db_order.pickup_lng,
#         "dropoff_lat": db_order.dropoff_lat,
#         "dropoff_lng": db_order.dropoff_lng,
#         "surge":       surge,
#     })
#     return db_order

# @router.get("/{order_id}", response_model=OrderResponse)
# def get_order(order_id: str, db: Session = Depends(get_db)):
#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         raise HTTPException(404, "Order not found")
#     return order

# @router.get("/", response_model=list[OrderResponse])
# def list_orders(db: Session = Depends(get_db)):
#     return db.query(Order).all()

# @router.patch("/{order_id}/status", response_model=OrderResponse)
# def update_status(
#     order_id: str,
#     body: OrderStatusUpdate,
#     db: Session = Depends(get_db)
# ):
#     try:
#         order = update_order_status(order_id, body.status, db)
#     except ValueError as e:
#         raise HTTPException(400, str(e))
#     if not order:
#         raise HTTPException(404, "Order not found")
#     return order

# @router.get("/status/{status}", response_model=list[OrderResponse])
# def get_orders_by_status(status: str, db: Session = Depends(get_db)):
#     from models.order import OrderStatus
#     try:
#         status_enum = OrderStatus(status)
#     except ValueError:
#         raise HTTPException(400, f"Invalid status: {status}")
#     return db.query(Order).filter(Order.status == status_enum).all()


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.order import Order
from models.user import User
from schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from services.kafka_producer import publish_new_order
from services.order_service import update_order_status
from services.surge_service import surge_calculator
from services import driver_store
from middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)   # ← requires login
):
    available_count = len(driver_store.get_available_drivers())
    surge = surge_calculator.get_surge_multiplier(
        order.pickup_lat, order.pickup_lng, available_count
    )
    base_price  = 50.0
    final_price = round(base_price * surge, 2)

    surge_calculator.record_order(order.pickup_lat, order.pickup_lng)

    db_order = Order(
        **order.model_dump(),
        surge_multiplier=surge,
        base_price=base_price,
        final_price=final_price
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    publish_new_order({
        "order_id":    str(db_order.id),
        "pickup_lat":  db_order.pickup_lat,
        "pickup_lng":  db_order.pickup_lng,
        "dropoff_lat": db_order.dropoff_lat,
        "dropoff_lng": db_order.dropoff_lng,
        "surge":       surge,
    })
    return db_order


@router.get("/", response_model=list[OrderResponse])
def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_status(
    order_id: str,
    body: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        order = update_order_status(order_id, body.status, db)
    except ValueError as e:
        raise HTTPException(400, str(e))
    if not order:
        raise HTTPException(404, "Order not found")
    return order


@router.get("/status/{status}", response_model=list[OrderResponse])
def get_orders_by_status(status: str, db: Session = Depends(get_db)):
    from models.order import OrderStatus
    try:
        status_enum = OrderStatus(status)
    except ValueError:
        raise HTTPException(400, f"Invalid status: {status}")
    return db.query(Order).filter(Order.status == status_enum).all()
