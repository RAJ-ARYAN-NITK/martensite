from collections import deque
from datetime import datetime, timedelta
from typing import Dict
import threading

class SurgeCalculator:
    """
    Sliding window — tracks orders in last 10 mins per zone.
    Zone = rounded lat/lng to 2 decimal places (≈ 1km grid).
    """
    def __init__(self, window_minutes: int = 10):
        self.window     = timedelta(minutes=window_minutes)
        self.zones: Dict[str, deque] = {}
        self.lock       = threading.Lock()

    def _get_zone(self, lat: float, lng: float) -> str:
        """Round to 2 decimals → ~1.1km grid zones."""
        return f"{round(lat, 2)},{round(lng, 2)}"

    def _cleanup(self, zone: str):
        """Remove events outside the sliding window."""
        cutoff = datetime.utcnow() - self.window
        while self.zones[zone] and self.zones[zone][0] < cutoff:
            self.zones[zone].popleft()

    def record_order(self, lat: float, lng: float):
        """Record a new order in this zone."""
        zone = self._get_zone(lat, lng)
        with self.lock:
            if zone not in self.zones:
                self.zones[zone] = deque()
            self.zones[zone].append(datetime.utcnow())

    def get_surge_multiplier(
        self,
        lat: float,
        lng: float,
        available_drivers: int
    ) -> float:
        """
        Surge = demand / supply ratio in sliding window.
        Returns multiplier: 1.0 (normal) → 2.5 (peak surge)
        """
        zone = self._get_zone(lat, lng)
        with self.lock:
            if zone not in self.zones:
                return 1.0

            self._cleanup(zone)
            demand = len(self.zones[zone])

        supply = max(available_drivers, 1)
        ratio  = demand / supply

        # Surge tiers
        if ratio >= 4:   return 2.5
        elif ratio >= 3: return 2.0
        elif ratio >= 2: return 1.5
        elif ratio >= 1: return 1.2
        else:            return 1.0

    def get_zone_stats(self, lat: float, lng: float) -> dict:
        zone = self._get_zone(lat, lng)
        with self.lock:
            if zone not in self.zones:
                return {"zone": zone, "recent_orders": 0}
            self._cleanup(zone)
            return {
                "zone":          zone,
                "recent_orders": len(self.zones[zone]),
            }


# Singleton — one instance for the whole app
surge_calculator = SurgeCalculator()