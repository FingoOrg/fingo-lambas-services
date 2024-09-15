import json
from db.client import DynamoDBClient
from config.env import DYNAMODB_TABLE_NAME

db_client = DynamoDBClient(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    path_info = event["path_info"]
    
    # Retrieve user data from DynamoDB
    response = db_client.get_form_data({
        'user_id': path_info['user_id'],
        'path_id': path_info['path_id']
    })

    # Check for success or error in the response and ensure 'data' is handled properly
    if response['status'] == 'success':
        # If 'data' exists, use it; otherwise, use an empty list or message
        dynamodb_response = response.get('data', 'No data found')
    else:
        # Handle the error case
        dynamodb_response = response.get('message', 'Unknown error occurred')

    return {
        'statusCode': 200 if response['status'] == 'success' else 500,
        'body': json.dumps({
            'form_data': dynamodb_response['item']['form_data']
        })
    }
