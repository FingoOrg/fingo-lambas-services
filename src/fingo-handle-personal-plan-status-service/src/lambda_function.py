import json
from db.client import DynamoDBClient
from config.env import DYNAMODB_TABLE_NAME
import uuid

db_client = DynamoDBClient(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    response = db_client.complete_node({
        'user_id': event["user_id"],
        'node_id': event["node_id"]
    })

    return {
        'statusCode': 200 if response['status'] == 'success' else 500,
        'body': json.dumps(response)
    }