import json
from db.client import DynamoDBClient
from bedrock.client import BedrockClient
from config.env import DYNAMODB_TABLE_NAME

BEDROCK_MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'

db_client = DynamoDBClient(DYNAMODB_TABLE_NAME)
bedrock_client = BedrockClient(
    region_name='us-west-2', 
    max_tokens=4000, 
    temperature=0.7, 
    top_p=0.9, 
    top_k=50,
)

def lambda_handler(event, context):
    path_info = event["path_info"]
    eventuality_description = event['eventuality_description']
    amount = event['amount']

    bedrock_response = path_info['bedrock_response']
    
    response = db_client.get_form_data({
        'user_id': path_info['user_id'],
        'path_id': path_info['path_id']
    })

    if response['status'] == 'success':
        dynamodb_response = response.get('data', 'No data found')
    else:
        dynamodb_response = response.get('message', 'Unknown error occurred')


    llm_query = f"""
        You are a financial expert tasked with **adjusting a personalized financial plan** for a user who has encountered an unexpected financial event. The current plan includes savings and investment strategies, but certain steps need to be modified based on this new event.

        ### Current Financial Plan:
        Here is the current financial plan for the user:

        {json.dumps(bedrock_response, indent=2)}

        ### Eventuality:
        The user has experienced the following financial event:

        - **Description**: {eventuality_description}
        - **Amount spent**: {amount}

        This event requires changes to the financial plan. Specifically, you need to adjust the steps that have not yet been completed. Do not modify the steps that have already been marked as completed (those with `status: true`). Adjust the rest of the steps to reflect the financial impact of the unexpected event, redistributing the remaining savings or investment amounts, updating deadlines, or re-prioritizing actions as necessary.

        ### User's Financial Profile:
        The user provided the following information regarding their financial situation, which should also inform your adjustments:

        {json.dumps(dynamodb_response, indent=2)}

        ### Criteria for Adjustments:
        1. **Modify only incomplete steps**: Ensure that steps marked as `status: true` remain unchanged. Focus on adjusting the remaining steps.
        2. **Rebalance savings and investments**: Adjust the remaining financial steps, considering the amount spent on the unexpected event, and suggest how the user can stay on track with their financial goals.
        3. **Adjust amounts and deadlines**: Propose new amounts to save or invest, and update due dates if necessary to account for the financial setback.
        4. **Maintain a balance between savings and investments**: Ensure that the user still works toward both short-term and long-term goals despite the financial setback.
        5. **Actionable Steps**: Each adjusted step should remain actionable, with a clear amount to save or invest, an updated target date, and the type of financial action (savings or investment).

        ### Expected Output:
        Provide the updated financial plan in the following JSON structure:

        [
            {{
                "id": int,                 // Unique identifier for the step
                "title": "string",         // Title of the step
                "description": "string",   // Detailed explanation of the step
                "type": "investment" or "savings",  // Type of step
                "amount": float,           // Updated amount to save or invest
                "due_date": "YYYY-MM-DD",  // Updated target date for completion
                "status": bool             // Status: true if completed, false if not
            }},
            ...
        ]

        Make sure to propose a plan that helps the user overcome the financial event while still working toward their long-term goals.
    """


    bedrock_response = bedrock_client.invoke_anthropic_claude(BEDROCK_MODEL_ID, llm_query,)

    return {
        'statusCode': 200 if response['status'] == 'success' else 500,
        'body': json.dumps({
            'dynamodb_response': str(dynamodb_response),
            'bedrock_response': bedrock_response,
        })
    }
