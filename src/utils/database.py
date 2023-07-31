from typing import Annotated, Any, Union

import motor.motor_asyncio
from bson import ObjectId
from pydantic import AfterValidator, PlainSerializer, WithJsonSchema

from constants.database import DATABASE_NAME, MONGO_STRING

# handles _id field of mongodb
def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]

# db connection
def connect_to_mongo():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_STRING)
    db = client[DATABASE_NAME]
    return db
