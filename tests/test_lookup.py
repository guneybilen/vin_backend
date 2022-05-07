from fastapi.testclient import TestClient
import sys

sys.path.append('..')

from main import app

client = TestClient(app)


def test_lookup_for_success1():
    response = client.get("/vin/lookup/?vin=1XPWD40X1ED215307")
    assert response.status_code == 200
    assert response.json() == {
        "model_year": "2014",
        "id": 1,
        "make": "PETERBILT",
        "cached_result": True,
        "model": "388",
        "vin": "1XPWD40X1ED215307",
        "body_class": "Truck-Tractor"
    }


def test_lookup_for_success2():
    response = client.get("/vin/lookup/?vin=1XKWDB0X57J211825")
    assert response.status_code == 200
    assert response.json() == {
        "model_year": "2007",
        "id": 2,
        "make": "KENWORTH",
        "cached_result": True,
        "model": "W9 Series",
        "vin": "1XKWDB0X57J211825",
        "body_class": "Truck-Tractor"
    }


def test_lookup_for_success3():
    response = client.get("/vin/lookup/?vin=1XP5DB9X7XD487964")
    assert response.status_code == 200
    assert response.json() == {
       "id": 5,
       "model_year": "1999",
       "make": "PETERBILT",
       "cached_result": True,
       "model": "379",
       "vin": "1XP5DB9X7XD487964",
       "body_class": "Truck-Tractor"
    }


def test_lookup_for_404():
    response = client.get("/vin/lookup/?vin=11111111111111111")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "vehicle with the 11111111111111111 number could not be found"
    }
