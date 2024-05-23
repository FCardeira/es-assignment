from datetime import datetime
from fastapi import APIRouter
from fastapi.params import Depends
import json

from app.utils import call_step_function
from app.models import AppointmentCreate, DBUser, Appointment, Slot
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
    appointments = json.loads(output["body"])

    for appointment in appointments:
        appointment["state"] = await get_appointment_state(appointment["appointment_id"])

    return [Appointment(**item) for item in appointments]

@router.get("/{appointment_id}/state")
async def get_appointment_state(appointment_id: str) -> str:
    appointment_id = int(appointment_id)
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

@router.get("/slots")
async def get_occupied_slots(date: str, doctor: str, user: DBUser = Depends(get_current_user)) -> list:
    output = await call_step_function(
        settings.GET_APPOINTMENTS_ARN,
        {"date": date, "doctor": doctor},
    )
    appointments = json.loads(output["body"])

    return [Slot(date=appointment["date"], time=appointment["time"], doctor=appointment["doctor"]) for appointment in appointments]

@router.put("/{appointment_id}/pay")
async def pay_appointment(appointment_id: int, user: DBUser = Depends(get_current_user)
) -> None:

    output = await call_step_function(
        settings.UPDATE_APPOINTMENT_STATE_ARN,
        {
            "appointment_id": appointment_id,
            "new_state": "Confirmed"
        }
    )

@router.get("/{appointment_id}")
async def get_appointment(appointment_id: int, user: DBUser = Depends(get_current_user)) -> Appointment:
    output = await call_step_function(
        settings.GET_APPOINTMENTS_ARN,
        {"appointment_id": appointment_id},
    )
    appointments = json.loads(output["body"])
    appointment = appointments[0]

    appointment["state"] = await get_appointment_state(appointment["appointment_id"])
    return Appointment(**appointment)


manager_router = APIRouter(
    prefix="/manager/appointments",
    tags=["Manager Appointments"],
)


@manager_router.get("/")
async def manager_get_appointments() -> list:
    output = await call_step_function(
        settings.GET_APPOINTMENTS_ARN,
        {}
    )
    
    appointments = json.loads(output["body"])

    for appointment in appointments:
        appointment["state"] = await get_appointment_state(appointment["appointment_id"])

    return [Appointment(**item) for item in appointments]


@manager_router.put("/{appointment_id}/finish")
async def finish_appointment(appointment_id: int) -> None:
    output = await call_step_function(
        settings.UPDATE_APPOINTMENT_STATE_ARN,
        {
            "appointment_id": appointment_id,
            "new_state": "Finished"
        }
    )
    return None
