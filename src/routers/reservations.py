from datetime import datetime
from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.reservation import ReservationModel, UpdateReservationModel
from utils.auth import get_current_active_user
from utils.database import connect_to_mongo
from utils.utils import check_dates

db = connect_to_mongo()
router = APIRouter(
    tags=["reservations"], responses={}, dependencies=[Depends(get_current_active_user)]
)


# create reservation
@router.post(
    "/reservation",
    response_description="Creates a new reservation",
    response_model=ReservationModel,
)
async def create_reservation(reservation: ReservationModel = Body(...)) -> JSONResponse:
    reservation = jsonable_encoder(reservation)
    reservation.pop("_id")  # pop id so it auto generates in mongoDB

    for date in ["arrival", "departure"]:  # convert to datetime
        _s = reservation[date]
        reservation[date] = datetime.strptime(_s, "%Y-%m-%d")

    if check_dates(reservation["arrival"], reservation["departure"]) is False:
        raise HTTPException(
            status_code=500, detail="Arrival can not be same or older than departure."
        )

    new_reservation = await db["reservations"].insert_one(reservation)
    created_reservation = await db["reservations"].find_one(
        {"_id": new_reservation.inserted_id}
    )
    for field in ["_id", "arrival", "departure"]:
        created_reservation[field] = str(created_reservation[field])
    return JSONResponse(status_code=201, content=created_reservation)


# list all reservations
@router.get(
    "/reservation",
    response_description="Gets reservations",
    response_model=List[ReservationModel],
)
async def list_reservations(
    page: int = Query(1, gt=0),
    page_size: int = Query(100, le=200),
    numberId: str = Query(None),  # 1-2-3-4
    rooms: str = Query(None),  # 1-2-3-4
    status: str = Query(None),
    channel: str = Query(None),
    agency: str = Query(None),
    arrival: str = Query(None),  # YYYY-MM-DD
    departure: str = Query(None),  # YYYY-MM-DD
) -> List[ReservationModel]:
    skip = (page - 1) * page_size

    filters = {}
    if numberId and numberId != "":
        filters["numberId"] = int(numberId)

    if rooms:
        _s = rooms.split("-")
        rooms = [int(room) for room in _s]
        filters["rooms"] = {"$in": rooms}

    if status:
        filters["status"] = status

    if channel:
        filters["channel"] = channel

    if agency:
        filters["agency"] = agency

    if arrival:
        _a = datetime.strptime(arrival, "%Y-%m-%d")
        filters["arrival"] = {"$gte": _a}

    if departure:
        _d = datetime.strptime(departure, "%Y-%m-%d")
        filters["departure"] = {"$lte": _d}
    reservations = (
        await db["reservations"].find(filters).skip(skip).limit(page_size).to_list(None)
    )
    return reservations


# get a single reservation
@router.get(
    "/reservation/{numberId}",
    response_description="Gets a single reservation",
    response_model=ReservationModel,
)
async def get_reservation(numberId: str) -> ReservationModel:
    numberId = int(numberId)
    reservation = await db["reservations"].find_one({"numberId": numberId})
    if reservation is not None:
        return reservation
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Reservation with numberId '{numberId}' not found",
        )


# update a reservation
@router.put(
    "/reservation/{numberId}",
    response_description="Updates a reservation",
    response_model=ReservationModel,
)
async def update_reservation(
    numberId, reservation: UpdateReservationModel = Body(...)
) -> ReservationModel:
    numberId = int(numberId)
    reservation = jsonable_encoder(reservation)
    for date in ["arrival", "departure"]:  # convert to datetime
        _s = reservation[date]
        reservation[date] = datetime.strptime(_s, "%Y-%m-%d")

    update_result = await db["reservations"].update_one(
        {"numberId": numberId}, {"$set": dict(reservation)}
    )

    if update_result.modified_count == 1:
        if (
            updated_reservation := await db["reservations"].find_one(
                {"numberId": numberId}
            )
        ) is not None:
            return updated_reservation

    if (
        existing_reservation := await db["reservations"].find_one(
            {"numberId": numberId}
        )
    ) is not None:
        return existing_reservation


# delete reservation
@router.delete("/reservation/{numberId}", response_description="Delete a reservation")
async def delete_reservation(numberId: str) -> JSONResponse:
    numberId = int(numberId)
    delete_result = await db["reservations"].delete_one({"numberId": numberId})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=204, content=None)
