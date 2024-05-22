from datetime import datetime
from fastapi import APIRouter
from fastapi.params import Depends

from app.utils import call_step_function
from app.models import AppointmentCreate, DBUser
from app.auth import get_current_user


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.get("/user")
async def get_user_appointments(user: DBUser = Depends(get_current_user)) -> list:
    # TODO: Get appointments from the database
    output = await call_step_function(
        "arn:aws:states:us-east-1:431099602872:stateMachine:getAppointments",
        {"usermane": user.username},
    )

    return [AppointmentCreate(**item) for item in output]


@router.post("/")
async def create_appointments(
    appointment: AppointmentCreate, user: DBUser = Depends(get_current_user)
) -> AppointmentCreate:
    # TODO: Create appointment in the database
    return []


@router.get("/")
async def get_all_appointments(user: DBUser = Depends(get_current_user)) -> list:
    # TODO: Get appointments from the database
    return []


manager_router = APIRouter(
    prefix="/manager/appointments",
    tags=["Manager Appointments"],
)


@manager_router.get("/")
async def manager_get_appointments() -> list:
    # TODO: Get appointments from the database
    # output = await call_step_function(
    #     "",
    #     {},
    # )

    # return [AppointmentCreate(**item) for item in output]
    return []


@manager_router.put("/{appointment_id}")
async def mark_state() -> AppointmentCreate:
    # TODO: Get appointments from the database
    # output = await call_step_function(
    #     "",
    #     {},
    # )

    # return [AppointmentCreate(**item) for item in output]
    return None
