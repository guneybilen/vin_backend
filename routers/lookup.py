from fastapi import APIRouter, Depends, status, HTTPException
from db import actions
from sqlalchemy.orm import Session

import requests
import models
import db_settings

router = APIRouter(
    prefix="/vin",
    tags=["Vin Check or Create"]
)


@router.get("/lookup", status_code=status.HTTP_200_OK)
def check_from_cache(vin: str, db: Session = Depends(db_settings.get_db)):
    db_result = actions.check_from_cache(vin, db)
    if db_result:
        return db_result
    else:
        new_db_entry = retrieve_and_store(vin, db)
        return new_db_entry


def retrieve_and_store(vin: str, db: Session = Depends(db_settings.get_db)):
    vehicle = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json")
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"vehicle with the {vin} number could not be found")
    parsed_vehicle = vehicle.json()

    obj = models.Vin()
    obj.vin = vin

    for val in parsed_vehicle["Results"]:
        if val["Variable"] == "Make":
            obj.make = val["Value"]
        if val["Variable"] == "Model":
            obj.model = val["Value"]
        if val["Variable"] == "Model Year":
            obj.model_year = val["Value"]
        if val["Variable"] == "Body Class":
            obj.body_class = val["Value"]
        obj.cached_result = False

    actions.create_vehicle_in_db(obj, db)
    return obj
