from kafka import KafkaProducer
import json
import os
import logging

logger = logging.getLogger(__name__)

def get_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=os.getenv(
                "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
            ),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            request_timeout_ms=5000,
            api_version_auto_timeout_ms=5000,
            max_block_ms=5000
        )
        return producer
    except Exception as e:
        logger.error(f"Kafka connection failed: {e}")
        return None

def publish_new_order(order_data: dict):
    producer = get_producer()
    if producer:
        try:
            producer.send("new-orders", order_data)
            producer.flush()
            print(f"Published order: {order_data}")
        except Exception as e:
            print(f"Kafka publish failed: {e}")
    else:
        print("Kafka unavailable — skipping")

def publish_driver_assignment(assignment_data: dict):
    producer = get_producer()
    if producer:
        try:
            producer.send("driver-assignments", assignment_data)
            producer.flush()
            print(f"Published assignment: {assignment_data}")
        except Exception as e:
            print(f"Kafka publish failed: {e}")
    else:
        print("Kafka unavailable — skipping")

def publish_order_status_update(status_data: dict):
    producer = get_producer()
    if producer:
        try:
            producer.send("order-status-updates", status_data)
            producer.flush()
            print(f"Published status update: {status_data}")
        except Exception as e:
            print(f"Kafka publish failed: {e}")
    else:
        print("Kafka unavailable — skipping")