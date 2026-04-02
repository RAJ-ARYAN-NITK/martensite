from itertools import permutations
from services.distance import get_straight_line_km
from models.driver import Location
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def optimize_multi_stop_route(
    driver_location: Location,
    stops: list[Location],
    max_stops: int = 8       # brute force safe up to 8 stops
) -> tuple[list[Location], float]:
    """
    Travelling Salesman Problem (TSP) — brute force for small sets.
    Finds shortest path visiting all stops starting from driver location.
    O(n!) — only use for n ≤ 8, use nearest-neighbor heuristic for larger.
    """
    if not stops:
        return [], 0.0

    if len(stops) > max_stops:
        logger.warning(f"{len(stops)} stops — using nearest neighbor heuristic")
        return _nearest_neighbor(driver_location, stops)

    best_route    = None
    best_distance = float('inf')

    for perm in permutations(stops):
        # Distance: driver → first stop → ... → last stop
        total = get_straight_line_km(
            driver_location.lat, driver_location.lng,
            perm[0].lat, perm[0].lng
        )
        for i in range(len(perm) - 1):
            total += get_straight_line_km(
                perm[i].lat,     perm[i].lng,
                perm[i+1].lat,   perm[i+1].lng
            )

        if total < best_distance:
            best_distance = total
            best_route    = list(perm)

    return best_route, round(best_distance, 2)


def _nearest_neighbor(
    start: Location,
    stops: list[Location]
) -> tuple[list[Location], float]:
    """
    Greedy nearest neighbor heuristic for large stop counts.
    O(n²) — much faster than O(n!) for n > 8.
    """
    unvisited     = stops.copy()
    route         = []
    total_distance = 0.0
    current       = start

    while unvisited:
        # Find nearest unvisited stop
        nearest = min(
            unvisited,
            key=lambda s: get_straight_line_km(
                current.lat, current.lng, s.lat, s.lng
            )
        )
        dist           = get_straight_line_km(
            current.lat, current.lng, nearest.lat, nearest.lng
        )
        total_distance += dist
        route.append(nearest)
        current        = nearest
        unvisited.remove(nearest)

    return route, round(total_distance, 2)


def calculate_route_distance(
    start: Location,
    stops: list[Location]
) -> float:
    """Calculate total distance for a given route order."""
    if not stops:
        return 0.0

    total = get_straight_line_km(
        start.lat, start.lng, stops[0].lat, stops[0].lng
    )
    for i in range(len(stops) - 1):
        total += get_straight_line_km(
            stops[i].lat, stops[i].lng,
            stops[i+1].lat, stops[i+1].lng
        )
    return round(total, 2)