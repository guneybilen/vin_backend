from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

import requests

import models
import database
from repository import VIN

router = APIRouter(
    prefix="/vin",
    tags=["Vin Check or Create"]
)


class Obj():
    pass


@router.get("/lookup", status_code=status.HTTP_200_OK)
def check_from_cache(vin: str, db: Session = Depends(database.get_db)):
    db_result = VIN.check_from_cache(vin, db)
    if db_result:
        return db_result
    else:
        new_db_entry = retrieve_and_store(vin, db)
        return new_db_entry


def retrieve_and_store(vin: str, db: Session = Depends(database.get_db)):
    vehicle = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json")
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"vehicle with the {vin} number could not be found")
    parsed_vehicle = vehicle.json()

    obj = models.VIN()
    obj.vin = vin

    for keyval in parsed_vehicle["Results"]:
        if keyval["Variable"] == "Make":
            obj.make = keyval["Value"]
        if keyval["Variable"] == "Model":
            obj.model = keyval["Value"]
        if keyval["Variable"] == "Model Year":
            obj.model_year = keyval["Value"]
        if keyval["Variable"] == "Body Class":
            obj.body_class = keyval["Value"]
        obj.cached_result = False

    VIN.create_vehicle_in_db(obj, db)
    return obj
