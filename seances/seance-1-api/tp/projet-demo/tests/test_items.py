def test_create_item(client):
    response = client.post(
        "/items",
        json={
            "titre": "Sac à dos",
            "description": "Sac de randonnée",
            "tarif_jour": 10.0,
            "disponible": True,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["titre"] == "Sac à dos"
    assert data["tarif_jour"] == 10.0


def test_list_items(client, item):
    response = client.get("/items")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == item["id"]


def test_get_item(client, item):
    response = client.get(f"/items/{item['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == item["id"]


def test_get_unknown_item(client):
    response = client.get("/items/999")

    assert response.status_code == 404


def test_update_item(client, item):
    response = client.put(
        f"/items/{item['id']}",
        json={
            "titre": "Grande tente",
            "description": "Tente familiale",
            "tarif_jour": 25.0,
            "disponible": False,
        },
    )

    assert response.status_code == 200
    assert response.json()["titre"] == "Grande tente"
    assert response.json()["tarif_jour"] == 25.0
    assert response.json()["disponible"] is False


def test_partial_update_item(client, item):
    response = client.patch(
        f"/items/{item['id']}",
        json={"tarif_jour": 20.0},
    )

    assert response.status_code == 200
    assert response.json()["tarif_jour"] == 20.0
    assert response.json()["titre"] == item["titre"]


def test_delete_item(client, item):
    response = client.delete(f"/items/{item['id']}")

    assert response.status_code == 204

    response = client.get(f"/items/{item['id']}")

    assert response.status_code == 404


def test_delete_unknown_item(client):
    response = client.delete("/items/999")

    assert response.status_code == 404


def test_item_validation(client):
    response = client.post(
        "/items",
        json={
            "titre": "A",
            "tarif_jour": -5,
        },
    )

    assert response.status_code == 422


def test_item_extra_field_forbidden(client):
    response = client.post(
        "/items",
        json={
            "titre": "Sac",
            "tarif_jour": 10.0,
            "unknown": "test",
        },
    )

    assert response.status_code == 422


def test_list_items_filter_available(client):
    client.post(
        "/items",
        json={
            "titre": "Tente",
            "tarif_jour": 15.0,
            "disponible": True,
        },
    )

    client.post(
        "/items",
        json={
            "titre": "Vélo",
            "tarif_jour": 20.0,
            "disponible": False,
        },
    )

    response = client.get("/items?disponible=true")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["titre"] == "Tente"


def test_list_items_search(client):
    client.post(
        "/items",
        json={
            "titre": "Tente rouge",
            "tarif_jour": 15.0,
        },
    )

    client.post(
        "/items",
        json={
            "titre": "Vélo noir",
            "tarif_jour": 20.0,
        },
    )

    response = client.get("/items?q=tente")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["titre"] == "Tente rouge"