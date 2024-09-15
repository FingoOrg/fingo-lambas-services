import json

def lambda_handler(event, context):
    """AWS Lambda handler."""
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Fingo Register Eventuality Service!')
    }