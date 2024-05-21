from datetime import datetime
from fastapi import APIRouter

from app.db.models import AppointmentModel
from app.db.dynamo import create_appointment


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


# @router.get()
# async def create_appointment(appointment: AppointmentModel) -> AppointmentModel:
#     # Logic to create an appointment
#     return appointment


@router.get("/")
async def get_appointments() -> list[AppointmentModel]:
    # Logic to create an appointment
    return []


@router.post("/")
async def create_appointment(appointment: AppointmentModel) -> AppointmentModel:
    db_appointment = await create_appointment(appointment)
    return db_appointment


@router.get("/{appointment_id}/")
async def get_appointment(appointment_id: int) -> AppointmentModel:
    # Logic to get an appointment by ID
    appointment = AppointmentModel(
        id=appointment_id,
        user_id=1,
        specialty="physiotherapy",
        appointment_date=datetime.now(),
        status="pending",
    )
    return appointment
