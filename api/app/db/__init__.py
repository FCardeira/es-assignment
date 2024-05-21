# from app.db.sql import get_db
from app.db.dynamo import get_dynamodb_resource
from app.db.dynamo import create_appointment

# get_db = get_db
get_dynamodb_resource = get_dynamodb_resource

create_appointment = create_appointment