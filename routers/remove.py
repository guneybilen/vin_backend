"""
The remove module: Delegates removing vehicle
data from the cache to db/actions.py
"""

import db_settings
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db import actions


router = APIRouter(
    prefix="/vin",
    tags=["Vin Remove From DB"]
)


@router.get("/remove", status_code=status.HTTP_200_OK)
def remove_from_cache(vin: str, db: Session = Depends(db_settings.get_db)):
    """
    sends the necessary data to db/actions.py.
    Notice: db/actions.py remove function can raise HTTPException without
    returning a result to this function.

    :param vin: vehicle identification (vin) string input.
    :param db: database instance.
    :return: json object.
    """
    returned_result = actions.remove(vin, db)
    return {"vin": vin, "cached_delete_success": returned_result}
