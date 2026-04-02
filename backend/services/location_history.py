from collections import deque
from datetime import datetime
from typing import Dict

class DriverLocationHistory:
    """
    Circular buffer — stores last N locations per driver.
    deque(maxlen=N) auto-discards oldest when full. O(1) append.
    """
    def __init__(self, max_per_driver: int = 100):
        self.max_size = max_per_driver
        self._history: Dict[str, deque] = {}

    def record(self, driver_id: str, lat: float, lng: float):
        if driver_id not in self._history:
            self._history[driver_id] = deque(maxlen=self.max_size)

        self._history[driver_id].append({
            "lat": lat,
            "lng": lng,
            "timestamp": datetime.utcnow().isoformat()
        })

    def get_history(self, driver_id: str, last_n: int = 10) -> list:
        if driver_id not in self._history:
            return []
        history = list(self._history[driver_id])
        return history[-last_n:]

    def get_latest(self, driver_id: str) -> dict:
        if driver_id not in self._history or not self._history[driver_id]:
            return {}
        return self._history[driver_id][-1]

    def clear(self, driver_id: str):
        if driver_id in self._history:
            self._history[driver_id].clear()


# Singleton
location_history = DriverLocationHistory(max_per_driver=100)