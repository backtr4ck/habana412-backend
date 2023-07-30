from datetime import datetime
from typing import List

import pymongo
from fastapi import Body, FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.reservation import ReservationModel, UpdateReservationModel
from utils.database import connect_to_mongo

# initialize FastAPI and database
app = FastAPI()
db = connect_to_mongo()


# create reservation
@app.post(
    "/reservation",
    response_description="Creates a new reservation",
    response_model=ReservationModel,
)
async def create_reservation(reservation: ReservationModel = Body(...)):
    reservation = jsonable_encoder(reservation)
    reservation.pop("_id")

    try:
        new_reservation = await db["reservations"].insert_one(reservation)
        created_reservation = await db["reservations"].find_one(
            {"_id": new_reservation.inserted_id}
        )
        created_reservation["_id"] = str(created_reservation["_id"])
        return JSONResponse(status_code=201, content=created_reservation)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Duplicated numberId")
    except pymongo.errors.ConnectionFailure:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error. Error: {e}"
        )


# list all reservations
@app.get(
    "/reservation",
    response_description="Gets reservations",
    response_model=List[ReservationModel],
)
async def list_reservations(
    page: int = Query(1, gt=0),
    page_size: int = Query(100, le=200),
    rooms: str = Query(None),  # 1-2-3-4
    status: str = Query(None),
    channel: str = Query(None),
    agency: str = Query(None),
    arrival: str = Query(None),  # YYYY_MM-DD
    departure: str = Query(None),  # YYYY_MM-DD
):
    try:
        skip = (page - 1) * page_size
        filters = {}

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
            _s = arrival.split("-")
            year = int(_s[0])
            month = int(_s[1])
            day = int(_s[2])
            arrival = datetime(year, month, day)
            filters["arrival"] = {"$gte": arrival}

        if departure:
            _s = departure.split("-")
            year = int(_s[0])
            month = int(_s[1])
            day = int(_s[2])
            departure = datetime(year, month, day)
            filters["departure"] = {"$lte": departure}

        reservations = (
            await db["reservations"]
            .find(filters)
            .skip(skip)
            .limit(page_size)
            .to_list(None)
        )
        return reservations
    except pymongo.errors.ConnectionFailure:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error. Error: {e}"
        )


# get a single reservation
@app.get(
    "/reservation/{numberId}",
    response_description="Gets a single reservation",
    response_model=ReservationModel,
)
async def get_reservation(numberId):
    numberId = int(numberId)
    try:
        if (
            reservation := await db["reservations"].find_one({"numberId": numberId})
        ) is not None:
            return reservation
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Reservation with numberId '{numberId}' not found",
            )
    except pymongo.errors.ConnectionFailure:
        raise HTTPException(
            status_code=500, detail="Could not connect to the database."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error. Error: {e}"
        )


# update a reservation
@app.put(
    "/reservation/{numberId}",
    response_description="Updates a reservation",
    response_model=ReservationModel,
)
async def update_reservation(numberId, reservation: UpdateReservationModel = Body(...)):
    try:
        numberId = int(numberId)

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

        raise KeyError
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Reservation with numberId {numberId} not found"
        )
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid numberId. It should be an integer."
        )
    except pymongo.errors.ConnectionFailure:
        raise HTTPException(
            status_code=500, detail="Could not connect to the database."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error. Error {e}")


# delete reservation
@app.delete("/reservation/{numberId}", response_description="Delete a reservation")
async def delete_reservation(numberId: str):
    try:
        numberId = int(numberId)
        delete_result = await db["reservations"].delete_one({"numberId": numberId})

        if delete_result.deleted_count == 1:
            return JSONResponse(status_code=204, content=None)

        raise HTTPException(
            status_code=404
        )  # TODO esta gilada hace que no se raisee el error. Hay que reescribir todas las funciones sin usar el if poronga ese

    except HTTPException:
        HTTPException(
            status_code=404, detail=f"Reservation with numberId {numberId} not found"
        )
    except pymongo.errors.ConnectionFailure:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal server error. Error: {e}"
        )
