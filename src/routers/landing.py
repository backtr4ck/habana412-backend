from fastapi import APIRouter, HTTPException
from jose import jwt

from constants.auth import JWT_SECRET_KEY

router = APIRouter(tags=["landing"], responses={})


@router.post("/", response_description="Check if auth_token is valid")
async def check_token(token=None):
    if token:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            if decoded_token:
                return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Token invalid. Error: {e}")
    else:
        raise HTTPException(status_code=404, detail="No token provided")
