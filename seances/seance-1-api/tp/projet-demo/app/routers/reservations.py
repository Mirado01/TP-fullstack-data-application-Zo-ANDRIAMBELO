from fastapi import APIRouter, HTTPException, Query
from app.schemas.reservation import ReservationCreate, ReservationRead

router = APIRouter(prefix="/reservations", tags=["reservations"])

FAKE_DB: dict[int, dict] = {}


@router.post("", response_model=ReservationRead, status_code=201)
def create_reservation(payload: ReservationCreate):
    reservation_id = max(FAKE_DB.keys(), default=0) + 1

    reservation = {
        "id": reservation_id,
        **payload.model_dump(),
        "statut": "active",
    }

    FAKE_DB[reservation_id] = reservation
    return reservation


@router.get("", response_model=list[ReservationRead])
def list_reservations(
    item_id: int | None = None,
    limit: int = Query(default=20, ge=1, le=100),
):
    reservations = list(FAKE_DB.values())

    if item_id is not None:
        reservations = [
            reservation
            for reservation in reservations
            if reservation["item_id"] == item_id
        ]

    return reservations[:limit]


@router.get("/{reservation_id}", response_model=ReservationRead)
def get_reservation(reservation_id: int):
    reservation = FAKE_DB.get(reservation_id)

    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail=f"Reservation {reservation_id} introuvable",
        )

    return reservation


@router.post("/{reservation_id}/annuler", response_model=ReservationRead)
def cancel_reservation(reservation_id: int):
    reservation = FAKE_DB.get(reservation_id)

    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail=f"Reservation {reservation_id} introuvable",
        )

    if reservation["statut"] == "annulee":
        raise HTTPException(
            status_code=409,
            detail="Reservation déjà annulée",
        )

    reservation["statut"] = "annulee"
    return reservation