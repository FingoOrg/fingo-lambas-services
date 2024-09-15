import json
from decimal import Decimal
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

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

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

        {json.dumps(bedrock_response, indent=2, default=decimal_default)}

        ### Eventuality:
        The user has experienced the following financial event:

        - **Description**: {eventuality_description}
        - **Amount spent**: {amount}

        This event requires changes to the financial plan. Specifically, you need to adjust the steps that have not yet been completed. **Do not modify or remove** the steps that have already been marked as completed (those with `status: true`). These steps must remain in the same position within the plan. Adjust the rest of the steps to reflect the financial impact of the unexpected event, redistributing the remaining savings or investment amounts, updating deadlines, or re-prioritizing actions as necessary.

        ### User's Financial Profile:
        The user provided the following information regarding their financial situation, which should also inform your adjustments:

        {json.dumps(dynamodb_response, indent=2, default=decimal_default)}

        ### Criteria for Adjustments:
        1. **Modify only incomplete steps**: Ensure that steps marked as `status: true` remain unchanged and stay in the same position. Focus on adjusting the remaining steps.
        2. **Rebalance savings and investments**: Adjust the remaining financial steps, considering the amount spent on the unexpected event, and suggest how the user can stay on track with their financial goals.
        3. **Adjust amounts and deadlines**: Propose new amounts to save or invest, and update due dates if necessary to account for the financial setback.
        4. **Maintain a balance between savings and investments**: Ensure that the user still works toward both short-term and long-term goals despite the financial setback.
        5. **Actionable Steps**: Each adjusted step should remain actionable, with a clear amount to save or invest, an updated target date, and the type of financial action (savings or investment).

        ### Important Instructions for JSON Structure:
        It is **critical** that the output is a **fully valid JSON**. Please strictly follow these guidelines:
        1. Ensure every opening has a matching closing and every `[` has a matching `]`.
        2. Every field must be correctly formatted as `"key": value`.
        3. Strings must be enclosed in double quotes `"`, and no extra commas should be present.
        4. Ensure that numeric values are properly formatted as numbers without quotes.
        5. Every JSON object must have the required fields: `id`, `title`, `description`, `type`, `amount`, `due_date`, and `status`.
        6. **Do not add any extra text, explanations, or commentary**. Return only the **pure JSON structure**, nothing else.
        7. **Steps that are marked as completed (with `status: true`) must remain in their original position and should not be modified or removed.**

        ### Expected Output:
        Please only return the **JSON structure** of the updated financial plan. Do not include any additional explanations or formatting other than the JSON structure. The JSON should follow this format:

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

        Make sure that **only** the updated JSON structure is returned as the output, without any additional text or explanation. Ensure that the structure is fully valid JSON with no missing brackets or commas, and that completed steps remain unchanged and in their original positions.
    """




    bedrock_response = bedrock_client.invoke_anthropic_claude(BEDROCK_MODEL_ID, llm_query,)

    return {
        'statusCode': 200 if response['status'] == 'success' else 500,
        'body': json.dumps({
            'dynamodb_response': dynamodb_response,
            'bedrock_response': bedrock_response,
        }, default=decimal_default)
    }