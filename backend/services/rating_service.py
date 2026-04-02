import heapq
from typing import Optional
from db import SessionLocal
from models.driver import Driver
import logging

logger = logging.getLogger(__name__)

# In-memory min heap: (distance, driver_id) — used for fast assignment
# Min heap always gives us the closest driver in O(log n)
_driver_heap: list = []


def build_driver_heap(drivers_with_distances: list[tuple[float, object]]):
    """
    Build a min heap from (distance, driver) pairs.
    O(n) to build, O(log n) to pop nearest.
    """
    heap = [(dist, idx, driver) for idx, (dist, driver) in enumerate(drivers_with_distances)]
    heapq.heapify(heap)
    return heap


def pop_nearest(heap: list) -> Optional[tuple]:
    """Get nearest driver in O(log n)."""
    if not heap:
        return None
    dist, _, driver = heapq.heappop(heap)
    return driver, dist


def rate_driver(driver_id: str, rating: float) -> Optional[Driver]:
    """
    Update driver's average rating using running average formula:
    new_avg = (old_avg * total + new_rating) / (total + 1)
    """
    if not 1.0 <= rating <= 5.0:
        raise ValueError("Rating must be between 1.0 and 5.0")

    db = SessionLocal()
    try:
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            return None

        # Running average — no need to store all ratings
        total  = driver.total_ratings or 0
        old_avg = driver.rating or 5.0

        new_avg = ((old_avg * total) + rating) / (total + 1)

        driver.rating        = round(new_avg, 2)
        driver.total_ratings = total + 1
        db.commit()
        db.refresh(driver)

        logger.info(f"Driver {driver_id} rated {rating} → new avg: {new_avg:.2f}")
        return driver
    finally:
        db.close()


def increment_trip_count(driver_id: str):
    """Called when a trip is completed."""
    db = SessionLocal()
    try:
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if driver:
            driver.total_trips = (driver.total_trips or 0) + 1
            db.commit()
    finally:
        db.close()


def get_top_drivers(limit: int = 10) -> list[Driver]:
    """Get top rated drivers using min heap (inverted for max)."""
    db = SessionLocal()
    try:
        drivers = db.query(Driver).filter(Driver.is_available == True).all()

        # Max heap using negative ratings
        heap = [(-d.rating, idx, d) for idx, d in enumerate(drivers)]
        heapq.heapify(heap)

        top = []
        for _ in range(min(limit, len(heap))):
            _, _, driver = heapq.heappop(heap)
            top.append(driver)

        return top
    finally:
        db.close()