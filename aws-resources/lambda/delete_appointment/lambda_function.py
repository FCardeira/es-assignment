import json
import pymysql

# Configuration values
rds_host = "es-clinic.cptjijpjcdzx.us-east-1.rds.amazonaws.com"
rds_user = "admin"
rds_password = "W3kUFrKIThZLo7Q8Rsz5"
rds_db_name = "esclinic"

def lambda_handler(event, context):
    appointment_id = event.get('appointment_id')
    print(event)
    try:
        # Establish a connection to the RDS instance
        connection = pymysql.connect(
            host=rds_host,
            user=rds_user,
            password=rds_password,
            db=rds_db_name
        )
         
        # Create a cursor object
        cursor = connection.cursor()

        delete_query = "DELETE FROM APPOINTMENTS WHERE id = %s ;"
        
        print(delete_query)
        
        # Execute the query
        cursor.execute(delete_query, (appointment_id, ))
        
        # Commit the transaction
        connection.commit();
        
        # Close the connection
        cursor.close()
        connection.close()
        
        return {
            'statusCode': 200,
            'body': json.dumps({ "message": "Deleted successfuly" })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
