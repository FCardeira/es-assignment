import json
import pymysql
import boto3
from datetime import datetime
import botocore.session

# Configuration values
rds_host = "es-clinic.cptjijpjcdzx.us-east-1.rds.amazonaws.com"
rds_user = "admin"
rds_password = "W3kUFrKIThZLo7Q8Rsz5"
rds_db_name = "esclinic"
dynamodb_table_name = "AppointmentsState"
dynamodb_region = "us-east-1"


def lambda_handler(event, context):
    patient_username = event.get('username')
    doctor = event.get('doctor')
    appointment_date = event.get('date')  # Expected format: dd/MM/yyyy
    appointment_time = event.get('time')  # Expected format: HH:mm

    try:
        # Combine date and time into a single datetime object if both are provided
        if appointment_date and appointment_time:
            combined_datetime = datetime.strptime(f"{appointment_date} {appointment_time}", "%d/%m/%Y %H:%M")
        else:
            combined_datetime = None

        # Establish a connection to the RDS instance
        connection = pymysql.connect(
            host=rds_host,
            user=rds_user,
            password=rds_password,
            database=rds_db_name
        )

        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # Start building the SQL query
        sql = "SELECT id as 'appointment_id', patient_username, doctor, speciality, DATE(date) as 'date', TIME(date) as 'time' FROM APPOINTMENTS"
        conditions = []
        parameters = []

        # Add conditions based on provided parameters
        if patient_username:
            conditions.append("patient_username = %s")
            parameters.append(patient_username)
        if doctor:
            conditions.append("doctor = %s")
            parameters.append(doctor)
        if combined_datetime:
            conditions.append("date = %s")
            parameters.append(combined_datetime)

        # Combine the conditions with AND operator if there are any
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        
        print("Before execute")
        cursor.execute(sql, parameters)
        print("After execute")

        # Fetch all results
        result = cursor.fetchall()
        print("Fetched?")
        print(result)
        
        for appointment in result:
            date_str = appointment['date'].strftime("%d/%m/%Y")
            time_str = (datetime.min + appointment['time']).strftime("%H:%M")
            appointment['date'] = date_str
            appointment['time'] = time_str

        # Close the connection
        cursor.close()
        connection.close()

        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }