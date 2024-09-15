import boto3
from botocore.exceptions import ClientError

class DynamoDBClient:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_form_data(self, item):
        try:

            response = self.table.get_item(
                Key = {
                    "path_id": item['path_id'], 
                    "user_id": item['user_id']
                }
            )

            return {
                'status': 'success',
                'response': response
            }
        
        except ClientError as e:
            return {
                'status': 'error',
                'message': e.response['Error']['Message']
            }