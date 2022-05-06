from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class VIN(Base):
    __tablename__ = "vins"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String)
    make = Column(String)
    model = Column(String)
    model_year = Column(String)
    body_class = Column(String)
    cached_result = Column(Boolean)
