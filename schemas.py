from pydantic import BaseModel
from typing import Optional


class VINBase(BaseModel):
    id: int
    vin: str
    make: str
    model: str
    model_year: str
    body_class: str
    cached_result: Optional[bool] = None


class VINSchema(VINBase):
    class Config():
        orm_mode = True
