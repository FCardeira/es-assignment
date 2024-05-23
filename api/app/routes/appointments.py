from datetime import datetime
from fastapi import APIRouter
from fastapi.params import Depends
import json

from app.utils import call_step_function
from app.models import AppointmentCreate, DBUser, Appointment
from app.auth import get_current_user
from app.settings import settings


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.get("/user")
async def get_user_appointments(user: DBUser = Depends(get_current_user)) -> list:
    output = await call_step_function(
        settings.GET_APPOINTMENTS_ARN,
        {"username": user.username},
    )
    breakpoint()

    appointments = json.loads(output["body"])


    return [AppointmentCreate(**item) for item in appointments]

@router.get("/{appointment_id}/state")
async def get_appointment_state(appointment_id: int) -> str:
    output = await call_step_function(
        settings.GET_APPOINTMENT_STATE_ARN,
        {"appointment_id": appointment_id},
    )
    return output

@router.post("/")
async def create_appointments(
    appointment: AppointmentCreate, user: DBUser = Depends(get_current_user)
) -> Appointment:

    output = await call_step_function(
        settings.SCHEDULE_APPOINTMENT_ARN,
        {
            "username": user.username,
            "doctor": appointment.doctor,
            "date": appointment.date,
            "time": appointment.time,
            "speciality": appointment.speciality,
        }
    )

    return Appointment(appointment_id=str(output["appointment_id"]), doctor=output["doctor"], date=output["date"], time=output["time"], speciality=output["speciality"], state="Waiting for payment")


@router.get("/")
async def get_all_appointments(user: DBUser = Depends(get_current_user)) -> list:
    # TODO: Get appointments from the database
    return []

@router.put("/{appointment_id}/pay")
async def pay_appointment(appointment_id: int, user: DBUser = Depends(get_current_user)
) -> None:

    output = await call_step_function(
        settings.UPDATE_APPOINTMENT_STATE_ARN,
        {
            "appointment_id": appointment_id,
            "state": "Confirmed"
        }
    )


manager_router = APIRouter(
    prefix="/manager/appointments",
    tags=["Manager Appointments"],
)


@manager_router.get("/")
async def manager_get_appointments() -> list:
    output = await call_step_function(
        settings.GET_APPOINTMENTS_ARN
    )
    return []


@manager_router.put("/{appointment_id}/finish")
async def finish_appointment(appointment_id: int) -> None:
    output = await call_step_function(
        settings.UPDATE_APPOINTMENT_STATE_ARN,
        {
            "appointment_id": appointment_id,
            "state": "Finished"
        }
    )
    return None
