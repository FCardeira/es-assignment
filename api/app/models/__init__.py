from pydantic import EmailStr, BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone_number: str


class UserRead(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreateResponse(BaseModel):
    username: str
    email: str
    phone_number: str


class LoginResponse(BaseModel):
    user: UserCreateResponse
    token: str
    exp: datetime | None


class DBUser(BaseModel):
    username: str
    password: str
    email: str
    phone_number: str
    exp: int | None = None  # expiration date


class AppointmentCreate(BaseModel):
    doctor: str
    date: str
    time: str
    speciality: str

class Appointment(BaseModel):
    appointment_id: str
    doctor: str
    date: str
    time: str
    speciality: str
    state: str | None = None
