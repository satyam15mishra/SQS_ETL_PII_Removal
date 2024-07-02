import boto3
import psycopg2
import json
from datetime import datetime
from utils import mask_value

# awscli local setup with boto3 (make sure botocore and boto3 versions are compatible)
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566')

# local sqs URL
queue_url = 'http://localhost:4566/000000000000/login-queue'

## setting up the connection and cursor for postgres
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def get_messages():
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=5
    )
    return response.get('Messages', [])

def load_body(message):
    body = json.loads(message['Body'])
    print("RAW MESSAGE: ", message)
    print("FLATTENED MESSAGE: ", body, "\n")
    
    # Check if 'create_date' key exists in the message body
    if 'create_date' not in body:
        try:
            user_id = body['user_id']
            device_type = body['device_type']
            masked_ip = mask_value(body['ip'])
            masked_device_id = mask_value(body['device_id'])
            locale = body['locale']
            app_version = parse_version(body['app_version'])
            create_date = datetime.today().date().strftime('%Y-%m-%d')

            ## using tuple (data structure) to insert data in psql table
            row_tuple = (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)

            cur.execute(
                """
                INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                row_tuple
            )
            conn.commit()
        except KeyError as e:
            print(f"KeyError: {e}. Skipping message:", body)
    else:
        print("'create_date' found in message:", body)

## function to handle app version (removing decimals to make the storage easier)
def parse_version(version_str):
    parts = version_str.split('.')
    try:
        version_int = int(''.join(parts))
    except ValueError:
        version_int = None
    return version_int

def main():
    while True:
        print("Fetching messages from SQS...")
        messages = get_messages()
        print(f"Received {len(messages)} messages")

        ## end the script if no further messages are received
        if len(messages) == 0:
            return 1 

        for message in messages:
            load_body(message)

if __name__ == '__main__':
    main()
