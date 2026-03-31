from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.driver import Driver
from services.redis_service import update_driver_location, set_driver_available

router = APIRouter(prefix="/drivers", tags=["drivers"])

@router.get("/")
def list_drivers(db: Session = Depends(get_db)):
    return db.query(Driver).all()

@router.put("/{driver_id}/location")
def update_location(driver_id: str, lat: float, lng: float,
                    db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    # Update in Redis (fast) and PostgreSQL (permanent)
    update_driver_location(driver_id, lat, lng)
    driver.current_lat = lat
    driver.current_lng = lng
    db.commit()

    return {"message": "Location updated"}

@router.put("/{driver_id}/availability")
def update_availability(driver_id: str, available: bool,
                        db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    set_driver_available(driver_id, available)
    driver.is_available = available
    db.commit()

    return {"message": f"Driver marked as {'available' if available else 'busy'}"}