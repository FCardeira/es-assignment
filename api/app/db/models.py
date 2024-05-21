from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserModel(BaseModel):
    id: int | None = Field(None, description="Unique identifier for the user")
    username: str = Field(..., description="User's login name")
    password: str = Field(..., description="Hashed password for authentication")
    email: EmailStr = Field(..., description="User's email address")
    phone_number: str = Field(..., description="User's phone number")
    created_at: datetime | None = Field(
        None, description="Timestamp for when the user was created"
    )
    updated_at: datetime | None = Field(
        None, description="Timestamp for when the user was last updated"
    )
    face_image_url: str | None = Field(
        None, description="URL to the user's face image stored in S3"
    )


class AppointmentModel(BaseModel):
    id: int | None = Field(None, description="Unique identifier for the appointment")
    user_id: int = Field(..., description="Foreign key linking to the User model")
    specialty: str = Field(
        ..., description="Type of service (e.g., physiotherapy, therapeutic massage)"
    )
    doctor: str | None = Field(None, description="Name of the doctor")
    appointment_date: datetime = Field(
        ..., description="Date and time of the appointment"
    )
    status: str = Field(
        ...,
        description="Current status of the appointment (e.g., pending, paid, completed)",
    )
    created_at: datetime | None = Field(
        None, description="Timestamp for when the appointment was created"
    )
    updated_at: datetime | None = Field(
        None, description="Timestamp for when the appointment was last updated"
    )


class PaymentModel(BaseModel):
    id: int | None = Field(None, description="Unique identifier for the payment")
    appointment_id: int = Field(
        ..., description="Foreign key linking to the Appointment model"
    )
    amount: float = Field(..., description="Amount to be paid")
    payment_method: str = Field(
        ..., description="Method of payment (e.g., MBWay, Multibanco)"
    )
    status: str = Field(
        ..., description="Payment status (e.g., pending, completed, failed)"
    )
    payment_reference: str | None = Field(
        None, description="Reference number for Multibanco or phone number for MBWay"
    )
    invoice_number: str | None = Field(
        None, description="Generated invoice number after payment"
    )
    created_at: datetime | None = Field(
        None, description="Timestamp for when the payment was created"
    )
    updated_at: datetime | None = Field(
        None, description="Timestamp for when the payment was last updated"
    )


class FaceRecognitionModel(BaseModel):
    id: int | None = Field(None, description="Unique identifier")
    user_id: int = Field(..., description="Foreign key linking to the User model")
    rekognition_id: str = Field(..., description="Identifier used by AWS Rekognition")
    created_at: datetime | None = Field(
        None, description="Timestamp for when the recognition data was created"
    )
    updated_at: datetime | None = Field(
        None, description="Timestamp for when the recognition data was last updated"
    )


class LogModel(BaseModel):
    id: int | None = Field(None, description="Unique identifier for the log entry")
    user_id: int | None = Field(
        None, description="Foreign key linking to the User model"
    )
    action: str = Field(..., description="Description of the action performed")
    timestamp: datetime = Field(..., description="When the action occurred")
    details: str | None = Field(None, description="Additional details about the action")


class JWTTokenModel(BaseModel):
    id: int | None = Field(None, description="Unique identifier for the token")
    user_id: int = Field(..., description="Foreign key linking to the User model")
    token: str = Field(..., description="The JWT token")
    created_at: datetime = Field(
        ..., description="Timestamp for when the token was created"
    )
    expires_at: datetime = Field(
        ..., description="Timestamp for when the token expires"
    )


class NotificationModel(BaseModel):
    id: int | None = Field(None, description="Unique identifier for the notification")
    user_id: int = Field(..., description="Foreign key linking to the User model")
    type: str = Field(..., description="Type of notification (e.g., SMS, email)")
    content: str = Field(..., description="Content of the notification")
    status: str = Field(..., description="Notification status (e.g., sent, failed)")
    created_at: datetime | None = Field(
        None, description="Timestamp for when the notification was created"
    )
    updated_at: datetime | None = Field(
        None, description="Timestamp for when the notification was last updated"
    )
