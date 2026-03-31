from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.order import Order
from schemas.order import OrderCreate, OrderResponse
from services.kafka_producer import publish_new_order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Publish to Kafka
    publish_new_order({
        "order_id": str(db_order.id),
        "pickup_lat": db_order.pickup_lat,
        "pickup_lng": db_order.pickup_lng,
        "dropoff_lat": db_order.dropoff_lat,
        "dropoff_lng": db_order.dropoff_lng,
    })

    return db_order

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()