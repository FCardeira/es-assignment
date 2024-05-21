import aioboto3

from app.db.models import AppointmentModel, JWTTokenModel, UserModel
from app.settings import settings


async def get_dynamodb_resource():
    session = aioboto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME,
    )
    async with session.resource("dynamodb", use_ssl=True) as dynamodb:
        yield dynamodb


async def create_appointment(appointment: AppointmentModel):
    async for dynamodb in get_dynamodb_resource():
        table = await dynamodb.Table("Appointment")
        await table.put_item(Item=appointment.model_dump())


async def create_jwt_token(jwt_token: JWTTokenModel):
    async for dynamodb in get_dynamodb_resource():
        table = await dynamodb.Table("JWTTokens")
        await table.put_item(Item=jwt_token.model_dump())


async def get_jwt_token(token_id: str):
    async for dynamodb in get_dynamodb_resource():
        table = await dynamodb.Table("JWTTokens")
        response = await table.get_item(Key={"id": token_id})
        return response.get("Item")


async def delete_jwt_token(token_id: str):
    async for dynamodb in get_dynamodb_resource():
        table = await dynamodb.Table("JWTTokens")
        await table.delete_item(Key={"id": token_id})


async def create_user(user: UserModel):
    async for dynamodb in get_dynamodb_resource():
        table = await dynamodb.Table("Users")
        await table.put_item(Item=user.model_dump())


async def get_user_by_username(username: str):
    async for dynamodb in get_dynamodb_resource():
        table = await dynamodb.Table("Users")
        response = await table.query(
            IndexName="username-index",
            KeyConditionExpression="username = :username",
            ExpressionAttributeValues={":username": username},
        )
        items = response.get("Items")
        return items[0] if items else None
