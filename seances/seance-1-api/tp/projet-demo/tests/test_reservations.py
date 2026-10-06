def test_create_reservation(client, item):
    response = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-15",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["item_id"] == item["id"]
    assert data["statut"] == "active"


def test_list_reservations(client, item):
    client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-15",
        },
    )

    response = client.get("/reservations")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_filter_reservations_by_item(client, item):
    client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-15",
        },
    )

    response = client.get(f"/reservations?item_id={item['id']}")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_reservation(client, item):
    create_response = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-15",
        },
    )

    reservation_id = create_response.json()["id"]

    response = client.get(f"/reservations/{reservation_id}")

    assert response.status_code == 200
    assert response.json()["id"] == reservation_id


def test_get_unknown_reservation(client):
    response = client.get("/reservations/999")

    assert response.status_code == 404


def test_invalid_reservation_dates(client, item):
    response = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-15",
            "date_fin": "2026-10-10",
        },
    )

    assert response.status_code == 422


def test_cancel_reservation(client, item):
    create_response = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-15",
        },
    )

    reservation_id = create_response.json()["id"]

    response = client.post(
        f"/reservations/{reservation_id}/annuler"
    )

    assert response.status_code == 200
    assert response.json()["statut"] == "annulee"


def test_cancel_reservation_twice(client, item):
    create_response = client.post(
        "/reservations",
        json={
            "item_id": item["id"],
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-15",
        },
    )

    reservation_id = create_response.json()["id"]

    client.post(f"/reservations/{reservation_id}/annuler")

    response = client.post(
        f"/reservations/{reservation_id}/annuler"
    )

    assert response.status_code == 409


def test_reservation_invalid_item_id(client):
    response = client.post(
        "/reservations",
        json={
            "item_id": 0,
            "date_debut": "2026-10-10",
            "date_fin": "2026-10-15",
        },
    )

    assert response.status_code == 422