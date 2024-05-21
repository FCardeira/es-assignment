# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from fastapi import Depends, HTTPException
from uuid import uuid4
from fastapi import HTTPException
from fastapi.routing import APIRouter

# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from sqlalchemy.orm import Session
# from api.app.db.sql import User
# from app.db import get_db

from app.db.models import UserModel
from app.models import Token, UserRead, UserCreate, TokenData
from app.db.dynamo import create_user, get_user_by_username

router = APIRouter(
    prefix="/auth",
    tags=["Authtentication"],
)


@router.post("/register")
async def register(user: UserCreate) -> UserRead:

    return UserRead


@router.post("/login")
async def register(user: UserRead) -> TokenData:
    existing_user = await get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # hashed_password = get_password_hash(user.password)
    user_model = UserModel(
        id=str(uuid4()),
        username=user.username,
        email=user.email,
        hashed_password=user.password,
    )
    await create_user(user_model)

    return UserModel(
        id=user_model.id,
        username=user_model.username,
        email=user_model.email,
        created_at=user_model.created_at,
        updated_at=user_model.updated_at,
    )


# @router.post("/token")
# async def login_for_access_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(SessionLocal),
# ) -> Token:
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/users/me", response_model=UserRead)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# # Password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # JWT settings
# SECRET_KEY = "mysecretkey"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def get_user(db, username: str):
#     return db.query(User).filter(User.username == username).first()


# def authenticate_user(db, username: str, password: str):
#     user = get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.password):
#         return False
#     return user


# async def get_current_user(
#     token: str = Depends(oauth2_scheme), db: Session = Depends(SessionLocal)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     return current_user
