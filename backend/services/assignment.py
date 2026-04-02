# from typing import Optional
# from datetime import datetime
# from models.driver import DriverSchema, Location, AssignmentResult, DriverStatus
# from services import driver_store
# from services.distance import get_straight_line_km, get_driving_info

# def find_nearest_driver(pickup: Location, vehicle_type: Optional[str] = None):
#     available = driver_store.get_available_drivers(vehicle_type)
#     if not available:
#         return None

#     candidates = sorted(
#         available,
#         key=lambda d: get_straight_line_km(
#             d.current_location.lat, d.current_location.lng,
#             pickup.lat, pickup.lng
#         )
#     )

#     refined = []
#     for driver in candidates[:3]:
#         driving_km, _ = get_driving_info(
#             driver.current_location.lat, driver.current_location.lng,
#             pickup.lat, pickup.lng
#         )
#         actual = driving_km or get_straight_line_km(
#             driver.current_location.lat, driver.current_location.lng,
#             pickup.lat, pickup.lng
#         )
#         refined.append((driver, actual))

#     refined.sort(key=lambda x: x[1])
#     return refined[0]

# def assign_driver(order_id: str, pickup: Location, dropoff: Location, vehicle_type: Optional[str] = None):
#     result = find_nearest_driver(pickup, vehicle_type)
#     if not result:
#         return None

#     driver, dist_to_pickup = result
#     driver_store.update_driver_status(driver.driver_id, DriverStatus.ON_TRIP)

#     driving_km, duration_mins = get_driving_info(
#         pickup.lat, pickup.lng, dropoff.lat, dropoff.lng
#     )

#     return AssignmentResult(
#         order_id=order_id,
#         driver_id=driver.driver_id,
#         driver_name=driver.name,
#         driver_phone=driver.phone,
#         pickup_location=pickup,
#         dropoff_location=dropoff,
#         straight_line_km=get_straight_line_km(pickup.lat, pickup.lng, dropoff.lat, dropoff.lng),
#         driving_distance_km=driving_km,
#         estimated_duration_mins=duration_mins,
#         distance_to_pickup_km=round(dist_to_pickup, 2),
#         assigned_at=datetime.utcnow().isoformat()
#     )

from typing import Optional
from datetime import datetime
from models.driver import DriverSchema, Location, AssignmentResult, DriverStatus
from services import driver_store
from services.distance import get_straight_line_km, get_driving_info
from services.rating_service import build_driver_heap, pop_nearest
import logging

logger = logging.getLogger(__name__)


def find_nearest_driver(
    pickup: Location,
    vehicle_type: Optional[str] = None
) -> Optional[tuple[DriverSchema, float]]:
    """
    Uses Min Heap for O(log n) nearest driver lookup.
    Also factors in driver rating for tiebreaking.
    """
    available = driver_store.get_available_drivers(vehicle_type)
    if not available:
        return None

    # Stage 1 — build heap with straight-line distances (cheap, no API)
    # Score = distance - (rating * 0.1) → slightly prefer higher rated drivers
    scored = []
    for driver in available:
        dist = get_straight_line_km(
            driver.current_location.lat, driver.current_location.lng,
            pickup.lat, pickup.lng
        )
        # Weighted score: distance penalized by rating bonus
        score = dist - (driver.rating * 0.1)
        scored.append((score, driver))

    # Build min heap — O(n)
    heap = build_driver_heap(scored)

    # Stage 2 — pop top 3 from heap, verify with real driving distance
    refined = []
    for _ in range(min(3, len(available))):
        result = pop_nearest(heap)
        if not result:
            break
        driver, _ = result

        driving_km, _ = get_driving_info(
            driver.current_location.lat, driver.current_location.lng,
            pickup.lat, pickup.lng
        )
        actual = driving_km or get_straight_line_km(
            driver.current_location.lat, driver.current_location.lng,
            pickup.lat, pickup.lng
        )
        refined.append((driver, actual))

    refined.sort(key=lambda x: x[1])
    return refined[0] if refined else None


def assign_driver(
    order_id: str,
    pickup: Location,
    dropoff: Location,
    vehicle_type: Optional[str] = None,
    surge_multiplier: float = 1.0
) -> Optional[AssignmentResult]:

    result = find_nearest_driver(pickup, vehicle_type)
    if not result:
        return None

    driver, dist_to_pickup = result
    driver_store.update_driver_status(driver.driver_id, DriverStatus.ON_TRIP)

    driving_km, duration_mins = get_driving_info(
        pickup.lat, pickup.lng, dropoff.lat, dropoff.lng
    )

    # Price = base(50) + distance_fee + surge
    base_price  = 50.0
    dist_fee    = (driving_km or 5.0) * 8   # ₹8 per km
    final_price = round((base_price + dist_fee) * surge_multiplier, 2)

    return AssignmentResult(
        order_id=order_id,
        driver_id=driver.driver_id,
        driver_name=driver.name,
        driver_phone=driver.phone,
        pickup_location=pickup,
        dropoff_location=dropoff,
        straight_line_km=get_straight_line_km(
            pickup.lat, pickup.lng, dropoff.lat, dropoff.lng
        ),
        driving_distance_km=driving_km,
        estimated_duration_mins=duration_mins,
        distance_to_pickup_km=round(dist_to_pickup, 2),
        surge_multiplier=surge_multiplier,
        final_price=final_price,
        assigned_at=datetime.utcnow().isoformat()
    )