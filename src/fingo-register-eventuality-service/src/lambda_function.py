import json
from db.client import DynamoDBClient
from config.env import DYNAMODB_TABLE_NAME

db_client = DynamoDBClient(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    path_info = event["path_info"]
    
    response = db_client.get_form_data({
        'user_id': path_info['user_id'],
        'path_id': path_info['path_id']
    })

    if response['status'] == 'success':
        dynamodb_response = response.get('data', 'No data found')
    else:
        dynamodb_response = response.get('message', 'Unknown error occurred')

    return {
        'statusCode': 200 if response['status'] == 'success' else 500,
        'body': json.dumps({
            'dynamodb_response': str(dynamodb_response)
        })
    }
