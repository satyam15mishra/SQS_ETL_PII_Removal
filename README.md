# ETL Project PII Removal and Building ETL off a SQS Queue


### Prerequisites

- Docker
- Docker-compose
- Python (i've used Python 3.12.3)
- AWS CLI Local
- PostgreSQL (psql)
- Boto3 (make sure boto3 and botocore versions are compatible, else we'll get 500 error while fetching sqs messages)
- Pyscopg2
- Utils
- Hashing Functions

### Instructions and Deployment

1. Clone the repository.
2. Go to the project.
3. Run `docker-compose up` to setup the localstack and postgres.
4. Install Python dependencies (make sure the versions are compatible according to your docker / boto3 and botocore:
    ```bash
    pip install -r requirements.txt
    ```
5. Run the ETL script:
    ```bash
    python main.py
    ```
6. Run postgres with psql -d postgres -U postgres -p 5432 -h localhost -W.
7. Enter password, and then you are good to query data!


## Thought Process

1. **Reading Messages**: Use `boto3` to interact with the SQS queue.
2. **Masking PII Data**: Use SHA-256 hashing to mask `device_id` and `ip` and handle duplicates.
3. **Writing to Postgres**: Used psycopg2 to establish conn and cursor in order to write sqs messages to postgres db.
4. **Error Handling and Logging**: Ensure appropriate error handling and logging for production readiness.


## Scaling

To handle a growing dataset, implement message batching, parallel processing, and database indexing.
Moreover, we can always use datalakes and warehouses instead of postgres if need arises or requirements change.

## Additional area of improvement for Production 

This can be put into production by hosting the `main.py` script to an ec2 service or on-prem servers.

## Assumptions

The fields being received in SQS messages are consistent.
If no field (0) is received, then we can assume that no more messages will be received in future (this can be modified in the script by triggering airflow DAGs if needed).

## Deanonymization of Masked Fields

The PII data can be recovered either by backing up masked fields or entire table in a safer environment, so that we can retrive them in future if needed.
But we need to make sure if it's compliant with local regulations / GLBA / CCPA / GDPR.

## Ideas

We can also setup email notifications if we receive anomalous data or new data.
Also, this can be further improved Airflow cron jobs.
