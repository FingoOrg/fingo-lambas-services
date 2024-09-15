import json
from dynamodb.client import DynamoDBClient
import os
import decimal

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

dynamodb_client = DynamoDBClient(os.environ['DYNAMODB_TABLE_NAME'])

def lambda_handler(event, context):
    """AWS Lambda Function to handle requests to the Personal Plans Service"""
    response = dynamodb_client.scan_item_by_user_id(os.environ['USER_ID'])

    return {
        'statusCode': 200,
        'body': json.dumps(response, default=decimal_default)
    }