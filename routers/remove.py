from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session
from db import actions
import db_settings


router = APIRouter(
    prefix="/vin",
    tags=["Vin Remove From DB"]
)


@router.get("/remove", status_code=status.HTTP_200_OK)
def remove_from_cache(vin: str, db: Session = Depends(db_settings.get_db)):
    returned_result = actions.remove(vin, db)
    return {"vin": vin, "cached_delete_success": returned_result}
