import json
from dynamodb.client import DynamoDBClient
from config.env import DYNAMODB_TABLE_NAME
import uuid

dynamodb_client = DynamoDBClient(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    """AWS Lambda handler."""
    response = dynamodb_client.insert_item(event)

    return {
        'statusCode': 200 if response['status'] == 'success' else 500,
        'body': json.dumps(response)
    }