# from sqlalchemy.orm import Session
# from models.order import Order, OrderStatus
# from services.kafka_producer import publish_order_status_update
# from typing import Optional
# import logging

# logger = logging.getLogger(__name__)

# # Valid status transitions — prevents jumping from pending → delivered
# VALID_TRANSITIONS = {
#     OrderStatus.PENDING:    [OrderStatus.ASSIGNED],
#     OrderStatus.ASSIGNED:   [OrderStatus.PICKED_UP],
#     OrderStatus.PICKED_UP:  [OrderStatus.IN_TRANSIT],
#     OrderStatus.IN_TRANSIT: [OrderStatus.DELIVERED],
#     OrderStatus.DELIVERED:  [],   # terminal state
# }

# def update_order_status(
#     order_id: str,
#     new_status: str,
#     db: Session,
#     driver_id: Optional[str] = None
# ) -> Optional[Order]:

#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         return None

#     try:
#         new_status_enum = OrderStatus(new_status)
#     except ValueError:
#         raise ValueError(f"Invalid status: {new_status}")

#     # Enforce valid transitions
#     allowed = VALID_TRANSITIONS.get(order.status, [])
#     if new_status_enum not in allowed:
#         raise ValueError(
#             f"Cannot transition from '{order.status.value}' to '{new_status}'. "
#             f"Allowed: {[s.value for s in allowed]}"
#         )

#     order.status = new_status_enum
#     if driver_id:
#         order.driver_id = driver_id

#     db.commit()
#     db.refresh(order)

#     # Broadcast status change to Kafka
#     publish_order_status_update({
#         "order_id":  str(order.id),
#         "status":    new_status,
#         "driver_id": order.driver_id,
#     })

#     logger.info(f"Order {order_id} → {new_status}")
#     return order

from sqlalchemy.orm import Session
from models.order import Order, OrderStatus
from services.kafka_producer import publish_order_status_update
from services.state_machine import is_valid_transition, get_allowed_transitions
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def update_order_status(
    order_id: str,
    new_status: str,
    db: Session,
    driver_id: Optional[str] = None
) -> Optional[Order]:

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None

    # Graph-based transition validation
    if not is_valid_transition(order.status, new_status):
        allowed = get_allowed_transitions(order.status)
        raise ValueError(
            f"Cannot transition from '{order.status.value}' to '{new_status}'. "
            f"Allowed: {allowed}"
        )

    try:
        order.status = OrderStatus(new_status)
    except ValueError:
        order.status = new_status

    if driver_id:
        order.driver_id = driver_id

    db.commit()
    db.refresh(order)

    publish_order_status_update({
        "order_id":  str(order.id),
        "status":    new_status,
        "driver_id": order.driver_id,
    })

    logger.info(f"Order {order_id} → {new_status}")
    return order