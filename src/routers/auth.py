from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models.auth import Token
from utils.auth import create_access_token, create_refresh_token, verify_password
from utils.database import connect_to_mongo

db = connect_to_mongo()
router = APIRouter()


@router.post(
    "/auth",
    description="Create access and refresh tokens for user",
    response_model=Token,
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.admin.find_one({'username': form_data.username})
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    hashed_pass = user["password"]
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    return {
        "access_token": create_access_token(user["username"]),
        "refresh_token": create_refresh_token(user["username"]),
    }
