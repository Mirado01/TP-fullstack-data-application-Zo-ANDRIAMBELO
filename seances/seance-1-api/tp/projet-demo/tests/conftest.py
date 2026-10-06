import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import items, reservations


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage():
    items.FAKE_DB.clear()
    reservations.FAKE_DB.clear()


@pytest.fixture
def item(client):
    response = client.post(
        "/items",
        json={
            "titre": "Tente de camping",
            "description": "Tente pour deux personnes",
            "tarif_jour": 15.0,
            "disponible": True,
        },
    )

    return response.json()