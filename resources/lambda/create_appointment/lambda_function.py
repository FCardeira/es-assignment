import json
import pymysql

# Configuration values
rds_host = "es-clinic.cptjijpjcdzx.us-east-1.rds.amazonaws.com"
rds_user = "admin"
rds_password = "W3kUFrKIThZLo7Q8Rsz5"
rds_db_name = "esclinic"

def lambda_handler(event, context):
    
    try:
        # Connect to MySQL server
        connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, database=rds_db_name)
        
        # Get payload from the event
        patient_username = event.get("patient_username")
        doctor = event.get("doctor")
        speciality = event.get("speciality")
        date = event.get("date")
        time = event.get("time")


        # Create a cursor object
        cursor = connection.cursor()

        # Query to insert a new appointment with sql injection protection
        insert_query = "INSERT INTO APPOINTMENTS (patient_username, doctor, speciality, date) VALUES (%s, %s, %s, %s);"

        # Execute the query
        cursor.execute(insert_query, (patient_username, doctor, speciality, date))
        
        # Commit the transaction
        connection.commit();

        # Get the last inserted id
        appointment_id = cursor.lastrowid
        
        # Return the response
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "appointment_id": appointment_id,
                "patient_username": patient_username,
                "doctor": doctor,
                "speciality": speciality,
                "date": date,
                "time": time
            })
        }

    except pymysql.Error as e:
        # Return the response
        response = {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }

    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()

    return response
