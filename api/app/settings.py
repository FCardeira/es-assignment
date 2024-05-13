import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IS_LOCAL: bool | None = False
    DEBUG: bool | None = False
    
    CORS_ALLOWED: list[str] | None = ["*"]

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/.env"
        validate_default = False


settings = Settings()
