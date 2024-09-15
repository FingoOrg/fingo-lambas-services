import json
from db.client import DynamoDBClient
from config.env import DYNAMODB_TABLE_NAME

db_client = DynamoDBClient(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    path_info = event["path_info"]
    nodes = path_info["bedrock_response"]
    
    # Actualizamos la información del path
    response = db_client.get_form_data({
        'user_id': path_info['user_id'],
        'path_id': path_info['path_id']
    })

    return {
        'statusCode': 200 if response['status'] == 'success' else 500,
        'body': json.dumps({
            'form_data': str(response['response'])
        })
    }
