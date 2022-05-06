from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session

import database
from repository import VIN

router = APIRouter(
    prefix="/vin",
    tags=["Vin Remove From DB"]
)


@router.get("/remove", status_code=status.HTTP_200_OK)
def remove_from_cache(vin: str, db: Session = Depends(database.get_db)):
    returned_result = VIN.remove(vin, db)
    return {"vin": vin, "cached_delete_success": returned_result}
