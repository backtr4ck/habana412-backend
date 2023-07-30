from datetime import datetime
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field

from utils.database import PyObjectId


class ReservationModel(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    numberId: int = Field(...)
    status: str = Field(...)
    name: str = Field(...)
    rooms: list = Field(...)
    channel: str = Field(...)
    agency: str = Field(...)
    arrival: datetime = Field(...)
    departure: datetime = Field(...)
    pax: int = Field(...)
    price: float = Field(...)
    tax: float = Field(...)
    notes: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "numberId": 1,
                "name": "Jane Doe",
                "status": "Confirmed",
                "rooms": [1, 2],
                "channel": "agency",
                "agency": "jelouu",
                "arrival": datetime(2023, 2, 1),
                "departure": datetime(2023, 2, 5),
                "pax": 4,
                "price": 345.30,
                "tax": 12.50,
                "notes": "arriving late at night",
            }
        }


class UpdateReservationModel(BaseModel):
    status: str = Field(default=None)
    name: str = Field(default=None)
    rooms: List[int] = Field(default=None)
    channel: str = Field(default=None)
    agency: str = Field(default=None)
    arrival: datetime = Field(default=None)
    departure: datetime = Field(default=None)
    pax: int = Field(default=None)
    price: float = Field(default=None)
    tax: float = Field(default=None)
    notes: str = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "status": "Confirmed",
                "rooms": [1, 2],
                "channel": "agency",
                "agency": "jelouu",
                "arrival": datetime(2023, 2, 1),
                "departure": datetime(2023, 2, 5),
                "pax": 4,
                "price": 345.30,
                "tax": 12.50,
                "notes": "arriving late at night",
            }
        }
