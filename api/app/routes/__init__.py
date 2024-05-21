from fastapi import APIRouter, status

from app.routes.appointments import router as appointments_router
from app.routes.auth import router as auth_router

appointments_router = appointments_router
auth_router = auth_router


base_router = APIRouter()


@base_router.get("/", status_code=200)
async def hello_world() -> str:
    return "Welcome to the ES API"


@base_router.get("/-/health", status_code=200)
async def healthcheck():
    """Healthcheck endpoint."""
    return status.HTTP_200_OK
