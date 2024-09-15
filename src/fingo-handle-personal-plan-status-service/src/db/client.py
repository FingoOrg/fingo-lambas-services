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
                    Key={
                        'user_id': item['user_id']
                    },
                    UpdateExpression="SET nodes.#n.completed = :val",
                    ConditionExpression="nodes.#n.node_id = :node_id",
                    ExpressionAttributeNames={
                        '#n': 'node_id'
                    },
                    ExpressionAttributeValues={
                        ':val': True,
                        ':node_id': item['user_id']
                    },
                    ReturnValues="UPDATED_NEW"
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