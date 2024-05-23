import boto3
import json
import asyncio
from fastapi import HTTPException

from settings import settings
from models import DBUser


client = boto3.client(
    service_name="stepfunctions",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION_NAME,
    aws_session_token=settings.AWS_SESSION_TOKEN,
    use_ssl=True,
)


async def call_step_function(arn: str, params: dict):
    response = client.start_execution(
        stateMachineArn=arn,
        input=json.dumps(params),
    )
    execution_arn = response["executionArn"]

    sleep = 0.5
    while True:
        execution_status = client.describe_execution(executionArn=execution_arn)
        status = execution_status["status"]
        if status == "SUCCEEDED":
            return json.loads(execution_status["output"])
        elif status == "RUNNING":
            await asyncio.sleep(sleep)
            sleep += 0.5
        elif status == "FAILED":
            raise HTTPException(status_code=400, detail=execution_status["error"])


async def get_user_dynamodb(username: str) -> DBUser:
    output = await call_step_function(
        settings.GET_USER_ARN,
        {"username": username},
    )
    return DBUser(**output)
