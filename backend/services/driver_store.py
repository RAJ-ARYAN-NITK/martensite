from typing import Optional
from sqlalchemy.orm import Session
from db import SessionLocal
from models.driver import Driver, DriverSchema, DriverStatus, Location
import uuid

def _get_db() -> Session:
    return SessionLocal()

def _to_schema(driver: Driver) -> DriverSchema:
    """Convert SQLAlchemy ORM object → Pydantic schema."""
    return DriverSchema(
        driver_id=str(driver.id),
        name=driver.name,
        phone=driver.phone,
        vehicle_type=driver.vehicle_type or "bike",
        status=DriverStatus.AVAILABLE if driver.is_available else DriverStatus.ON_TRIP,
        current_location=Location(
            lat=driver.current_lat or 0.0,
            lng=driver.current_lng or 0.0
        )
    )

def add_driver(driver: DriverSchema) -> DriverSchema:
    db = _get_db()
    try:
        db_driver = Driver(
            id=uuid.UUID(driver.driver_id),
            name=driver.name,
            phone=driver.phone,
            vehicle_type=driver.vehicle_type,
            current_lat=driver.current_location.lat,
            current_lng=driver.current_location.lng,
            is_available=True
        )
        db.add(db_driver)
        db.commit()
        db.refresh(db_driver)
        return _to_schema(db_driver)
    finally:
        db.close()

def get_driver(driver_id: str) -> Optional[DriverSchema]:
    db = _get_db()
    try:
        driver = db.query(Driver).filter(Driver.id == uuid.UUID(driver_id)).first()
        return _to_schema(driver) if driver else None
    finally:
        db.close()

def get_all_drivers() -> list[DriverSchema]:
    db = _get_db()
    try:
        return [_to_schema(d) for d in db.query(Driver).all()]
    finally:
        db.close()

def get_available_drivers(vehicle_type: Optional[str] = None) -> list[DriverSchema]:
    db = _get_db()
    try:
        query = db.query(Driver).filter(Driver.is_available == True)
        if vehicle_type:
            query = query.filter(Driver.vehicle_type == vehicle_type)
        return [_to_schema(d) for d in query.all()]
    finally:
        db.close()

def update_driver_location(driver_id: str, lat: float, lng: float) -> Optional[DriverSchema]:
    db = _get_db()
    try:
        driver = db.query(Driver).filter(Driver.id == uuid.UUID(driver_id)).first()
        if not driver:
            return None
        driver.current_lat = lat
        driver.current_lng = lng
        db.commit()
        db.refresh(driver)
        return _to_schema(driver)
    finally:
        db.close()

def update_driver_status(driver_id: str, status: DriverStatus) -> Optional[DriverSchema]:
    db = _get_db()
    try:
        driver = db.query(Driver).filter(Driver.id == uuid.UUID(driver_id)).first()
        if not driver:
            return None
        driver.is_available = (status == DriverStatus.AVAILABLE)
        db.commit()
        db.refresh(driver)
        return _to_schema(driver)
    finally:
        db.close()