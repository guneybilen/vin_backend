import pytest
import sys
import os
from fastapi.testclient import TestClient
from main import app
from config.test_database_settings import Base, engine
from routers import export
from pathlib import Path

sys.path.append('..')

client = TestClient(app)


@pytest.fixture()
def clear_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_parquet_file_created(monkeypatch):
    monkeypatch.chdir(f"{Path.cwd()}/config")

    monkeypatch.setattr(export, "SQLALCHEMY_DATABASE_URL", "sqlite:///test.db")
    response = client.get("/vin/export")

    with open("vin_records.parquet") as f:
        assert f.name == "vin_records.parquet"

    assert response.headers["Content-Type"] == "application/octet-stream"
    assert response.headers["Content-Disposition"] == "attachment; filename=vin_records.parquet"

    assert response.status_code == 200

    os.remove("vin_records.parquet")
    assert os.path.exists("vin_records.parquet") is False
