from pydantic import EmailStr, BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
