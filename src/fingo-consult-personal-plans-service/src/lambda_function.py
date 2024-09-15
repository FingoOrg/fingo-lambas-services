import json

def lambda_handler(event, context):
    """AWS Lambda Function to handle requests to the Personal Plans Service"""
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }