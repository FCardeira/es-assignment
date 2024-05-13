from logging import getLogger
from fastapi import APIRouter, status


log = getLogger(__name__)

router = APIRouter()


@router.get("/", status_code=200)
async def hello_world() -> str:
    return "Welcome to the ES API"


@router.get("/-/health", status_code=200)
async def healthcheck():
    """Healthcheck endpoint."""
    return status.HTTP_200_OK
