from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, landing, reservations, utils

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(reservations.router)
app.include_router(auth.router)
app.include_router(landing.router)
app.include_router(utils.router)
