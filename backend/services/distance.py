import requests
from geopy.distance import geodesic

def get_straight_line_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Haversine straight-line distance in km."""
    return round(geodesic((lat1, lng1), (lat2, lng2)).kilometers, 2)

def get_driving_info(lat1: float, lng1: float, lat2: float, lng2: float):
    """
    Returns (distance_km, duration_mins) via OSRM.
    Falls back to (None, None) on failure — never crashes assignment.
    """
    try:
        url = (
            f"http://router.project-osrm.org/route/v1/driving/"
            f"{lng1},{lat1};{lng2},{lat2}"           # OSRM needs lng,lat order
        )
        resp = requests.get(url, params={"overview": "false"}, timeout=5)
        if resp.status_code == 200:
            route = resp.json()["routes"][0]
            return (
                round(route["distance"] / 1000, 2),  # metres → km
                round(route["duration"] / 60, 2),    # seconds → mins
            )
    except Exception:
        pass
    return None, None