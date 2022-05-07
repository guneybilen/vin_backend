from db_settings import Base
from sqlalchemy import Column, Integer, String, Boolean


class Vin(Base):
    __tablename__ = "vin_records"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String)
    make = Column(String)
    model = Column(String)
    model_year = Column(String)
    body_class = Column(String)
    cached_result = Column(Boolean)
