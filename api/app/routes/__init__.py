from fastapi import APIRouter, status

from routes.auth import router as auth_router
from routes.appointments import router as appointments_router
from routes.appointments import manager_router as manager_appointments_router
from routes.payment import router as payment_router


appointments_router = appointments_router
manager_appointments_router = manager_appointments_router

auth_router = auth_router

payment_router = payment_router


base_router = APIRouter()


@base_router.get("/", status_code=200)
async def hello_world() -> str:
    return "Welcome to the ES API"


@base_router.get("/-/health", status_code=200)
async def healthcheck():
    """Healthcheck endpoint."""
    return status.HTTP_200_OK
