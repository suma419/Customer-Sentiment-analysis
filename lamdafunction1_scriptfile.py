import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
import json
import boto3
import base64
import uuid

s3 = boto3.client('s3')
bucket = 'kinesisbucket55'  # Updated bucket name

def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(payload)

        file_name = f"input/{uuid.uuid4()}.json"
        s3.put_object(Bucket=bucket, Key=file_name, Body=json.dumps(data))

    return {
        'statusCode': 200,
        'body': 'Records processed and saved to S3.'
    }
