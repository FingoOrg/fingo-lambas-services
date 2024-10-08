import boto3
from botocore.exceptions import ClientError

class DynamoDBClient:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_form_data(self, item):
        try:
            response = self.table.get_item(
                Key={
                    "path_id": item['path_id'], 
                    "user_id": item['user_id']
                }
            )

            if 'Item' in response:
                return {
                    'status': 'success',
                    'data': response['Item']['form_data']  # Fixed to return 'Item' (singular)
                }
            else:
                return {
                    'status': 'success',
                    'data': []  # Empty list if no item is found
                }
        
        except ClientError as e:
            return {
                'status': 'error',
                'message': e.response['Error']['Message']
            }

    def rewrite_node(self, item):
        try:

            br_quotes = str(item['bedrock_response']).replace("'", '"')
            br_bool = br_quotes.replace("True", "true")
            br_str = br_bool.replace("False", "false")

            response = self.table.update_item(
                Key={"path_id": item['path_id'], "user_id": item['user_id']},
                UpdateExpression="set bedrock_response=:br",
                ExpressionAttributeValues={":br": br_str},
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