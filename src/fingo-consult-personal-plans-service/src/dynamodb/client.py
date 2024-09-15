import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

class DynamoDBClient:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def query_item(self, path_id, user_id):
        try:
            response = self.table.query(
                KeyConditionExpression=Key('path_id').eq(path_id) & Key('user_id').eq(user_id)
            )
            if 'Items' in response:
                return {
                    'status': 'success',
                    'data': response['Items']
                }
            else:
                return {
                    'status': 'success',
                    'data': []
                }
        except ClientError as e:
            return {
                'status': 'error',
                'message': e.response['Error']['Message']
            }