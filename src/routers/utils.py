from fastapi import APIRouter, Depends, HTTPException

from utils.auth import get_current_active_user
from utils.database import connect_to_mongo

router = APIRouter(
    tags=["utils"], responses={}, dependencies=[Depends(get_current_active_user)]
)

db = connect_to_mongo()


@router.get("/numberid", response_description="Check latest numberId")
async def check_numberId():
    try:
        cursor = db["reservations"].find().sort("numberId", -1).limit(1)
        doc = await cursor.to_list(length=1)
        return doc[0]["numberId"]
    except Exception as e:
        HTTPException(status_code=500, detail=f"Error fetching numberId. {e}")
