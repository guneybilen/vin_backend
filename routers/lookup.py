"""
The lookup module:  Check by the vin string from the
database first and if no entry found in the database
retrieve through vPIC API and store in
the database.
"""

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
    """
    checks the vehicle with the entered vin string from the local database first
    and if not found calls a helper function to retrieve from vPIC API and store
    the newly created vehicle information in the local database.

    :param vin: vehicle identification (vin) string input.
    :param db: database instance.
    :return: either found database record or retrieved and stored newly
             created database record came back from the passed
             function.
    """
    db_result = actions.check_from_cache(vin, db)
    if db_result:
        return db_result
    else:
        new_db_entry = retrieve_and_store(vin, db)
        return new_db_entry


def retrieve_and_store(vin: str, db: Session = Depends(db_settings.get_db)):
    """
    A fresh check from vPIC API and if the vehicle found store in the
    local database and return result else return a 404 error.

    :param vin: vehicle identification string (vin) argument from the calling function.
    :param db: database instance.
    :return: either HTTPException or retrieved and stored newly
             created database record to the calling function.
    """
    vehicle = requests.get(f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevinextended/{vin}?format=json")
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
            if obj.make is None and obj.model is None and obj.model_year is None and obj.body_class is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"vehicle with the {vin} number could not be found")
        obj.cached_result = False

    actions.create_vehicle_in_db(obj, db)
    return obj
