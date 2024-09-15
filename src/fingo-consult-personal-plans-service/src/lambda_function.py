import json
from dynamodb.client import DynamoDBClient
import os
import decimal

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def sum_completed_amounts(response):
    savings_total = 0
    investment_total = 0
    
    bedrock_response = json.loads(response['data'][0]['bedrock_response'])
    
    for plan in bedrock_response:
        if plan['status'] == True:
            if plan['type'] == 'savings':
                savings_total += plan['amount']
            elif plan['type'] == 'investment':
                investment_total += plan['amount']
    
    return {
        'savings_total': savings_total,
        'investment_total': investment_total
    }

dynamodb_client = DynamoDBClient(os.environ['DYNAMODB_TABLE_NAME'])

def lambda_handler(event, context):
    """AWS Lambda Function to handle requests to the Personal Plans Service"""
    response = dynamodb_client.scan_item_by_user_id(os.environ['USER_ID'])
    completed_amount = sum_completed_amounts(response)

    return {
        'statusCode': 200,
        'body': json.dumps(response, default=decimal_default),
        'amounts': completed_amount
    }
