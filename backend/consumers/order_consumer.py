from kafka import KafkaConsumer
import json
import os
import logging
import threading
from db import SessionLocal
from models.order import Order, OrderStatus
from models.driver import Location
from services import assignment as assign_service
from services import driver_store
from services.kafka_producer import publish_driver_assignment

logger = logging.getLogger(__name__)

def process_order(order_data: dict):
    """Auto-assign nearest driver when a new order arrives."""
    db = SessionLocal()
    try:
        order_id = order_data["order_id"]
        pickup   = Location(lat=order_data["pickup_lat"],  lng=order_data["pickup_lng"])
        dropoff  = Location(lat=order_data["dropoff_lat"], lng=order_data["dropoff_lng"])

        # Find and assign nearest driver
        result = assign_service.assign_driver(
            order_id=order_id,
            pickup=pickup,
            dropoff=dropoff
        )

        if result:
            # Update order in DB with assigned driver + status
            order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                order.driver_id = result.driver_id
                order.status    = OrderStatus.ASSIGNED
                db.commit()
                logger.info(f"✅ Order {order_id} assigned to {result.driver_name}")

            # Broadcast assignment event to Kafka
            publish_driver_assignment({
                "order_id":              order_id,
                "driver_id":             result.driver_id,
                "driver_name":           result.driver_name,
                "driver_phone":          result.driver_phone,
                "driving_distance_km":   result.driving_distance_km,
                "estimated_duration_mins": result.estimated_duration_mins,
                "distance_to_pickup_km": result.distance_to_pickup_km,
            })
        else:
            logger.warning(f"⚠️  No drivers available for order {order_id}")

    except Exception as e:
        logger.error(f"Error processing order {order_data}: {e}")
        db.rollback()
    finally:
        db.close()


def start_order_consumer():
    """Runs in a background thread — consumes new-orders topic."""
    try:
        consumer = KafkaConsumer(
            "new-orders",
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            group_id="order-processor",
            auto_offset_reset="earliest",
            consumer_timeout_ms=1000,
        )
        logger.info("🎧 Order consumer started — listening on 'new-orders'")

        while True:
            for message in consumer:
                logger.info(f"📦 New order received: {message.value}")
                process_order(message.value)

    except Exception as e:
        logger.error(f"Kafka consumer failed: {e} — running without Kafka")


def start_consumer_thread():
    """Start consumer in background so it doesn't block FastAPI."""
    thread = threading.Thread(target=start_order_consumer, daemon=True)
    thread.start()
    return thread