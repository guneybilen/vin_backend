from fastapi import FastAPI
from routers import lookup, remove, export
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(lookup.router)
app.include_router(remove.router)
app.include_router(export.router)
