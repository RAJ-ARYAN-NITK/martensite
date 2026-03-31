from kafka import KafkaProducer
import json
import os

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_new_order(order_data: dict):
    producer.send("new-orders", order_data)
    producer.flush()
    print(f"Published order to Kafka: {order_data}")

def publish_driver_assignment(assignment_data: dict):
    producer.send("driver-assignments", assignment_data)
    producer.flush()
    print(f"Published assignment to Kafka: {assignment_data}")