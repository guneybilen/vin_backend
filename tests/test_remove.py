import pytest
import sys
from fastapi.testclient import TestClient
from main import app
from config.test_database_settings import Base, engine

sys.path.append('..')

client = TestClient(app)


@pytest.fixture()
def clear_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_remove_for_success1(clear_db):
    response = client.get("/vin/lookup/?vin=1XPWD40X1ED215307")
    assert response.status_code == 200

    data = response.json()

    assert data["model_year"] == "2014"
    assert data["make"] == "PETERBILT"
    assert data["cached_result"] is False
    assert data["model"] == "388"
    assert data["vin"] == "1XPWD40X1ED215307"
    assert data["body_class"] == "Truck-Tractor"

    response = client.get("/vin/remove/?vin=1XPWD40X1ED215307")
    assert response.status_code == 200
    assert response.json() == {
        "vin": "1XPWD40X1ED215307",
        "cached_delete_success": "removed successfully"
    }


def test_remove_for_success2(clear_db):
    response = client.get("/vin/lookup/?vin=1XKWDB0X57J211825")
    assert response.status_code == 200

    data = response.json()

    assert data["model_year"] == "2007"
    assert data["make"] == "KENWORTH"
    assert data["cached_result"] is False
    assert data["model"] == "W9 Series"
    assert data["vin"] == "1XKWDB0X57J211825"
    assert data["body_class"] == "Truck-Tractor"

    response = client.get("/vin/remove/?vin=1XKWDB0X57J211825")
    assert response.status_code == 200
    assert response.json() == {
        "vin": "1XKWDB0X57J211825",
        "cached_delete_success": "removed successfully"
    }


def test_remove_for_success3(clear_db):
    response = client.get("/vin/lookup/?vin=1XP5DB9X7XD487964")
    assert response.status_code == 200

    data = response.json()

    assert data["model_year"] == "1999"
    assert data["make"] == "PETERBILT"
    assert data["cached_result"] is False
    assert data["model"] == "379"
    assert data["vin"] == "1XP5DB9X7XD487964"
    assert data["body_class"] == "Truck-Tractor"

    response = client.get("/vin/remove/?vin=1XP5DB9X7XD487964")
    assert response.status_code == 200
    assert response.json() == {
        "vin": "1XP5DB9X7XD487964",
        "cached_delete_success": "removed successfully"
    }


def test_remove_for_404(clear_db):
    response = client.get("/vin/remove/?vin=11111111111111111")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "vehicle with the 11111111111111111 vin could not be found"
    }
