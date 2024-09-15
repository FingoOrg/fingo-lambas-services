import boto3
import os
from botocore.exceptions import ClientError

class DynamoDBClient:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def insert_item(self, form_data, model_response):
        try:
            response = self.table.put_item(Item={
                'user_id': os.environ['USER_ID'],
                'form_data': form_data,
                'bedrock_response': model_response
            })
            return {
                'status': 'success',
                'response': response
            }
        except ClientError as e:
            return {
                'status': 'error',
                'message': e.response['Error']['Message']
            }