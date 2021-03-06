from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas


def check_from_cache(vin, db: Session):
    vin = db.query(models.Vin).filter(models.Vin.vin == vin).first()
    return vin


def create_vehicle_in_db(vehicle: schemas.VINSchema, db: Session):
    new_vin = models.Vin(vin=vehicle.vin, make=vehicle.make,
                         model=vehicle.model, model_year=vehicle.model_year,
                         body_class=vehicle.body_class, cached_result=True)
    db.add(new_vin)
    db.commit()
    db.refresh(new_vin)
    return new_vin


def remove(vin: str, db: Session):
    found_vin = db.query(models.Vin).filter(models.Vin.vin == vin).first()
    if not found_vin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"vehicle with the {vin} vin could not be found")
    db.delete(found_vin)
    db.commit()
    return "removed successfully"
