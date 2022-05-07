from fastapi import FastAPI
from routers import lookup, remove, export
from db_settings import engine

import models

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(lookup.router)
app.include_router(remove.router)
app.include_router(export.router)
