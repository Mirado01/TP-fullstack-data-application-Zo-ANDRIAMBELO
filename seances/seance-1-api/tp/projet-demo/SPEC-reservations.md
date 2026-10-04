# Ressource : reservations

Fichiers :
- `app/schemas/reservation.py`
- `app/routers/reservations.py`

Stockage :
- dictionnaire en mémoire dans le router

## Schémas

- `ReservationCreate` : item_id (int, >= 1), date_debut (date), date_fin (date)
- `ReservationRead` : id, item_id, date_debut, date_fin, statut ("active" | "annulee")

## Routes

- POST `/reservations` → 201
- GET `/reservations` → 200
- GET `/reservations/{reservation_id}` → 200 / 404
- POST `/reservations/{reservation_id}/annuler` → 200 / 404 / 409

## Contraintes

- Aucun accès à FAKE_DB de items.
- response_model sur toutes les routes.
- Validation de `date_fin > date_debut` dans Pydantic.