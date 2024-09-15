import json
from db.client import DynamoDBClient
from config.env import DYNAMODB_TABLE_NAME
import uuid

db_client = DynamoDBClient(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    completed_id = event["completed_id"]
    path_info = event["path_info"]
    nodes = path_info["bedrock_response"]

    # Marcamos el path como completado
    for node in nodes:
        if node["id"] == completed_id:
            node["status"] = True

    # Establecemos las nuevas badges
    badges = path_info["badge"]

    # Actualizamos la información del path
    response = db_client.complete_node({
        'user_id': path_info['user_id'],
        'path_id': path_info['path_id'],
        'badge': badges,
        'bedrock_response': nodes
    })

    return {
        'statusCode': 200 if response['status'] == 'success' else 500,
        'body': json.dumps({
            'dynamodb_response': str(response['response'])
        })
    }