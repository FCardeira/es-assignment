import boto3
from fastapi import Depends
from fastapi.routing import APIRouter
from app.utils import call_step_function, get_user_dynamodb
from app.settings import settings
from app.models import UserRead, UserCreate, UserCreateResponse, LoginResponse, DBUser
from app.auth import create_access_token, get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authtentication"],
)


client = boto3.client(
    service_name="stepfunctions",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION_NAME,
    aws_session_token=settings.AWS_SESSION_TOKEN,
    use_ssl=True,
)


@router.post("/register")
async def register_user(user: UserCreate) -> UserCreateResponse:
    output = await call_step_function(
        "arn:aws:states:us-east-1:431099602872:stateMachine:userRegister",
        {
            "username": user.username,
            "password": user.password,
            "email": user.email,
            "phone_number": user.phone_number,
        },
    )
    return UserCreateResponse(**output)


@router.post("/login")
async def login(user: UserRead) -> LoginResponse:
    db_user = await get_user_dynamodb(user.username)

    data = db_user.model_dump()
    data.pop("exp", None)
    token, exp = create_access_token(data)

    # No need to persist the token in the db
    # Features we would gain by persisting tokens in the database:
    # Revoking Tokens: If you need to implement token revocation (e.g., logging out users or invalidating tokens before their expiration), you need a way to track and check tokens against a blacklist or revocation list.
    # Session Management: If you need to track user sessions for auditing or regulatory compliance, you might store token information along with session metadata in a database.
    # Additional Security: Persisting tokens allows you to implement additional security measures, such as ensuring a token is only valid for a single session or device.

    return LoginResponse(
        user=UserCreateResponse(
            username=db_user.username,
            email=db_user.email,
            phone_number=db_user.phone_number,
        ),
        token=token,
        exp=exp.timestamp(),
    )


@router.get("/me")
async def get_user(user: DBUser = Depends(get_current_user)) -> UserCreateResponse:
    return UserCreateResponse(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
    )
