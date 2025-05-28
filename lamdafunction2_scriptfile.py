import json
import boto3
import uuid
from decimal import Decimal

s3 = boto3.client('s3')
comprehend = boto3.client('comprehend', region_name='us-east-2')
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('SentimentResults')  # Make sure this table exists

def lambda_handler(event, context):
    # Get S3 object info
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Read file content from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    body = response['Body'].read().decode('utf-8')
    content = json.loads(body)

    results = []

    # Handle list of records
    if isinstance(content, list):
        for item in content:
            text = item.get('comment') or item.get('text')
            if not text:
                continue
            sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
            result = {
                'original': item,
                'sentiment': sentiment
            }
            results.append(result)

            # Save to DynamoDB (convert float to Decimal)
            table.put_item(
                Item={
                    'id': str(uuid.uuid4()),
                    'text': text,
                    'sentiment': sentiment['Sentiment'],
                    'scores': {k: Decimal(str(v)) for k, v in sentiment['SentimentScore'].items()}
                }
            )

    else:
        # Handle single record
        text = content.get('comment') or content.get('text')
        if not text:
            return {'statusCode': 400, 'body': 'No comment/text found'}
        sentiment = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        result = {
            'original': content,
            'sentiment': sentiment
        }
        results.append(result)

        # Save to DynamoDB (convert float to Decimal)
        table.put_item(
            Item={
                'id': str(uuid.uuid4()),
                'text': text,
                'sentiment': sentiment['Sentiment'],
                'scores': {k: Decimal(str(v)) for k, v in sentiment['SentimentScore'].items()}
            }
        )

    # Save sentiment results to processed/ folder
    output_key = key.replace('input/', 'processed/')
    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=json.dumps(results),
        ContentType='application/json'
    )

    return {
        'statusCode': 200,
        'body': f'{len(results)} sentiment result(s) saved to {output_key} and DynamoDB'
    }
