import boto3
import uuid
from botocore.exceptions import ClientError

class DynamoDBClient:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def complete_node(self, item):
        try:

            response = self.table.update_item(
                Key={"path_id": item['path_id'], "user_id": item['user_id']},
                UpdateExpression="set bedrock_response=:br, badges=:bg",
                ExpressionAttributeValues={":br": str(item['bedrock_response']), ":bg": item['badge']},
                ReturnValues="UPDATED_NEW",
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