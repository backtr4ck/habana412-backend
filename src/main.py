from fastapi import Body, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from models.reservation import ReservationModel
from utils.database import connect_to_mongo

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
    reservation.pop('_id')
    new_reservation = await db["reservations"].insert_one(reservation)
    created_reservation = await db["reservations"].find_one(
        {"_id": new_reservation.inserted_id}
    )
    created_reservation["_id"] = str(created_reservation["_id"])
    return JSONResponse(status_code=201, content=created_reservation)
