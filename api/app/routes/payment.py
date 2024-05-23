from datetime import datetime
from fastapi import APIRouter
from fastapi.params import Depends

from utils import call_step_function
from models import AppointmentCreate, DBUser
from auth import get_current_user


router = APIRouter(
    prefix="/appointments/{appointment_id}/payments",
    tags=["Payments"],
)


@router.put("/")
async def pay_appointment(user: DBUser = Depends(get_current_user)) -> list:
    pass
