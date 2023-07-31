from fastapi import FastAPI

from routers import auth, reservations

app = FastAPI()

# routers
app.include_router(reservations.router)
app.include_router(auth.router)
