import json
from dynamodb.client import DynamoDBClient
from bedrock.client import BedrockClient
from config.env import (
    DYNAMODB_TABLE_NAME,
    BEDROCK_MODEL_ID,
)

dynamodb_client = DynamoDBClient(DYNAMODB_TABLE_NAME)
bedrock_client = BedrockClient(
    region_name='us-west-2', 
    max_tokens=300, 
    temperature=0.7, 
    top_p=0.9, 
    top_k=50,
)

def lambda_handler(event, context):
    """AWS Lambda handler."""
    form_data = event['form_data']
    llm_query = "Using the following information, what is the best way to invest $1000 in the stock market?" + str(form_data)

    bedrock_response = bedrock_client.invoke_anthropic_claude(BEDROCK_MODEL_ID, llm_query,)
    dynamo_response = dynamodb_client.insert_item(
        form_data=form_data,
        model_response=bedrock_response,
    )

    return {
        'statusCode': 200,
        'body': json.dumps({
            'bedrock_response': bedrock_response,
            'dynamo_response': dynamo_response,
        }),
    }