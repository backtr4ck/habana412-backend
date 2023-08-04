from datetime import datetime

from fastapi import APIRouter, HTTPException
from jose import jwt

from constants.auth import JWT_SECRET_KEY

router = APIRouter(tags=["landing"], responses={})


@router.post("/", response_description="Check if auth_token is valid")
async def check_token(token=None):
    if token:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Token invalid. Error: {e}")
        decoded_exp = decoded_token["exp"]
        exp = datetime.fromtimestamp(decoded_exp)
        if exp < datetime.now():
            raise HTTPException(status_code=400, detail="Token expired or invalid")
        else:
            return True
    else:
        raise HTTPException(status_code=404, detail="No token provided")
