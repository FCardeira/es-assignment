from typing import Tuple
import boto3
import asyncio
from datetime import datetime, timedelta, UTC
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from pydantic import BaseModel
from fastapi import status

from app.settings import settings
from app.models import DBUser


SECRET_KEY = "es_very_secret_key_2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(user_date: dict) -> Tuple[str, datetime]:
    to_encode = user_date.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def verify_access_token(token: str, credentials_exception) -> DBUser:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.pop("username")
        token_data = DBUser(username=username, **payload)
        if token_data.exp is None:
            raise credentials_exception
        elif datetime.fromtimestamp(token_data.exp, tz=UTC) < datetime.now(UTC):
            # TODO: Cleanup db

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        _exp = datetime.fromtimestamp(token_data.exp, tz=UTC)
        print(f"Token expire = {_exp} -> {_exp - datetime.now(UTC)}")

    except JWTError:
        raise credentials_exception
    except KeyError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)) -> DBUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)
