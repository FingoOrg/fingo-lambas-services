import boto3
from botocore.exceptions import ClientError

class DynamoDBClient:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def insert_item(self, item):
        try:
            response = self.table.put_item(Item=item)
            return {
                'status': 'success',
                'response': response
            }
        except ClientError as e:
            return {
                'status': 'error',
                'message': e.response['Error']['Message']
            }