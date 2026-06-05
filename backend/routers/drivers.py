from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from datetime import datetime
import uuid
import json

from models.driver import (
    RegisterDriverRequest,
    UpdateLocationRequest,
    AssignDriverRequest,
    DriverSchema,
    DriverStatus,
)
from services import driver_store
from services import assignment as assign_service

router = APIRouter(prefix="/drivers", tags=["Drivers"])

# ── Active WebSocket connections {driver_id: websocket} ─────────────────────
active_connections: dict[str, WebSocket] = {}


@router.post("/register", response_model=DriverSchema, status_code=201)
def register_driver(req: RegisterDriverRequest):
    driver = DriverSchema(
        driver_id=str(uuid.uuid4()),
        name=req.name,
        phone=req.phone,
        vehicle_type=req.vehicle_type,
        current_location=req.current_location,
    )
    return driver_store.add_driver(driver)


@router.patch("/location")
def update_location(req: UpdateLocationRequest):
    driver = driver_store.update_driver_location(
        req.driver_id, req.current_location.lat, req.current_location.lng
    )
    if not driver:
        raise HTTPException(404, "Driver not found")
    return {"message": "Location updated", "driver_id": req.driver_id}


@router.patch("/{driver_id}/status")
def update_status(driver_id: str, status: DriverStatus):
    driver = driver_store.update_driver_status(driver_id, status)
    if not driver:
        raise HTTPException(404, "Driver not found")
    return {"message": f"Status updated to {status}", "driver_id": driver_id}


@router.get("/")
def list_drivers(status: DriverStatus = None):
    drivers = driver_store.get_all_drivers()
    if status:
        drivers = [d for d in drivers if d.status == status]
    return {"count": len(drivers), "drivers": drivers}


@router.post("/assign")
def assign_driver(req: AssignDriverRequest):
    result = assign_service.assign_driver(
        order_id=req.order_id,
        pickup=req.pickup_location,
        dropoff=req.dropoff_location,
        vehicle_type=req.vehicle_type,
    )
    if not result:
        raise HTTPException(503, "No available drivers right now.")
    return result


@router.post("/complete/{driver_id}")
def complete_trip(driver_id: str, order_id: str):
    driver = driver_store.update_driver_status(driver_id, DriverStatus.AVAILABLE)
    if not driver:
        raise HTTPException(404, "Driver not found")
    return {
        "message": "Trip completed, driver is now available",
        "driver_id": driver_id,
        "order_id": order_id,
        "completed_at": datetime.utcnow().isoformat(),
    }

