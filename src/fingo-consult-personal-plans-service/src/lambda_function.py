import json
from dynamodb.client import DynamoDBClient
import os

dynamodb_client = DynamoDBClient(os.environ['DYNAMODB_TABLE_NAME'])

def lambda_handler(event, context):
    """AWS Lambda Function to handle requests to the Personal Plans Service"""
    response = dynamodb_client.query_item(os.environ['USER_ID'])

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }