import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IS_LOCAL: bool | None = False
    DEBUG: bool | None = False
    
    CORS_ALLOWED: list[str] | None = ["*"]
    # DYNAMO_DB_PATH: str
    # POSTGRES_DB_PATH: str
    
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str | None = "eu-west-1"
    AWS_SESSION_TOKEN: str

    REGISTER_USER_ARN: str
    GET_USER_ARN: str
    UPDATE_APPOINTMENT_STATE_ARN: str
    SCHEDULE_APPOINTMENT_ARN: str
    GET_APPOINTMENTS_ARN: str
    GET_APPOINTMENT_STATE_ARN: str
    

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/.env"
        validate_default = False


settings = Settings()
