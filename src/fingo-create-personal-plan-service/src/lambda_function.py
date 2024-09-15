import json
from dynamodb.client import DynamoDBClient
from bedrock.client import BedrockClient
from config.env import (
    DYNAMODB_TABLE_NAME,
    BEDROCK_MODEL_ID,
)

dynamodb_client = DynamoDBClient(DYNAMODB_TABLE_NAME)

def lambda_handler(event, context):
    """AWS Lambda handler."""
    llm_query = event['llm_query']
    bedrock_client = BedrockClient(
        region_name='us-west-2', max_tokens=300,  
        temperature=0.7, top_p=0.9, top_k=50,
    )

    bedrock_response = bedrock_client.invoke_anthropic_claude(BEDROCK_MODEL_ID, llm_query,)

    dynamo_response = dynamodb_client.insert_item(
        llm_query, event['form_data'], bedrock_response,
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'bedrock_response': bedrock_response,
            'dynamo_response': dynamo_response,
        }),
    }