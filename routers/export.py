from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from pandas import read_sql
from db_settings import SQLALCHEMY_DATABASE_URL

router = APIRouter(
    prefix="/vin",
    tags=["Export From DB"]
)


def iter_file():
    with open("vin_records.parquet", mode="rb") as file_like:
        yield from file_like


@router.get("/export", status_code=status.HTTP_200_OK)
async def export_from_cache():
    data_frame = read_sql("SELECT * from vin_records", SQLALCHEMY_DATABASE_URL)
    data_frame.to_parquet("vin_records.parquet", index=False)

    response = StreamingResponse(iter_file(), media_type="application/octet-stream")
    response.headers["Content-Disposition"] = "attachment; filename=vin_records.parquet"

    return response
