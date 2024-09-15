import json
from dynamodb.client import DynamoDBClient
from config.env import DYNAMODB_TABLE_NAME
import uuid

dynamodb_client = DynamoDBClient(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    response = dynamodb_client.insert_item({
        'user_id': uuid.uuid4().hex,
        'event': event
    })

    return {
        'statusCode': 200 if response['status'] == 'success' else 500,
        'body': json.dumps(response)
    }