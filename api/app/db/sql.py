from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime, UTC

from app.settings import settings



engine = create_async_engine(settings.POSTGRES_DB_PATH, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


def timestamp_now():
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    created_at = Column(DateTime, default=timestamp_now)
    updated_at = Column(DateTime, default=timestamp_now)
    face_image_url = Column(String)


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    specialty = Column(String)
    doctor = Column(String)
    appointment_date = Column(DateTime)
    status = Column(String)
    created_at = Column(DateTime, default=timestamp_now)
    updated_at = Column(DateTime, default=timestamp_now)


class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    amount = Column(Float)
    payment_method = Column(String)
    status = Column(String)
    payment_reference = Column(String)
    invoice_number = Column(String)
    created_at = Column(DateTime, default=timestamp_now)
    updated_at = Column(DateTime, default=timestamp_now)


Base.metadata.create_all(bind=engine)
