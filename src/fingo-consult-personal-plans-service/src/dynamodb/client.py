import boto3
from botocore.exceptions import ClientError

class DynamoDBClient:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def scan_item_by_user_id(self, user_id):
        try:
            # Scan for items with the specified user_id
            response = self.table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr('user_id').eq(user_id)
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