"""
The export module: exports database to the client
browser in parquet formatted file (from HTTP protocol).
"""


import sqlalchemy.exc
from fastapi import APIRouter, status, HTTPException
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


@router.get("/export")
async def export_from_cache():
    """
    PREREQUISITE: information in the database that would be filled
    with the lookup process.
    this route creates parquet formatted file and streams this file as an
    attachment to the client browser (from HTTP protocol).
    :return: parquet formatted file.
    """

    try:
        data_frame = read_sql("SELECT * from vin_records", SQLALCHEMY_DATABASE_URL)
        data_frame.to_parquet("vin_records.parquet", index=False)

        response = StreamingResponse(iter_file(), media_type="application/octet-stream")
        response.headers["Content-Disposition"] = "attachment; filename=vin_records.parquet"

    except sqlalchemy.exc.OperationalError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="server error occurred.")

    return response
