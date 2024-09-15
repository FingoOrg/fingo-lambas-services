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
    max_tokens=1000, 
    temperature=0.7, 
    top_p=0.9, 
    top_k=50,
)

def lambda_handler(event, context):
    """AWS Lambda handler."""
    form_data = event['form_data']
    llm_query = f"""
        You are a financial expert tasked with creating a **detailed, personalized financial plan** for the user. The user has provided comprehensive information regarding their financial situation, including:

        - Monthly income
        - Monthly expenses (e.g., housing, food, transportation, etc.)
        - Current debts (e.g., student loans, credit card balances, mortgage)
        - Financial goals (both short-term and long-term)
        - Investment preferences and risk tolerance (e.g., conservative, moderate, aggressive)
        - Plans for major life events (e.g., buying a house, education, retirement)

        Below is a summary of the user's financial profile based on their responses:

        {form_data}

        ### Task:
        Your task is to generate a **step-by-step personal financial and investment plan** for the user. The plan must focus on both **savings** and **investment strategies**, clearly tailored to their goals. The steps should be **actionable**, realistic, and formatted in JSON.

        ### Criteria for the Plan:
        1. **Balance between short-term and long-term goals:** The steps must reflect goals such as building an emergency fund, reducing debt, or saving for retirement.
        2. **Savings Strategies:** The plan should include savings steps that align with the user’s financial situation, such as building an emergency fund, saving for a home, or retirement.
        3. **Investment Strategies:** Recommend investment options based on the user's risk tolerance and goals, such as stock market investments, bonds, or retirement accounts (e.g., 401(k), Roth IRA).
        4. **Actionable Steps:** Each step should include an amount of money to save or invest, a specific deadline, and a status (whether the step is completed or not).
        5. **Diversity in Steps:** The plan must include a mix of both savings and investment strategies, considering the user's financial goals and personal profile.
        
        ### Step Structure (JSON format):
        ```json
        [
            {{
                "id": int,                 // Unique identifier for the step (e.g., 1, 2, 3...)
                "title": "string",         // A concise title for the step (e.g., "Build Emergency Fund")
                "description": "string",   // Detailed explanation of the step and why it’s important
                "type": "investment" or "savings",  // Type of step: either investment or savings
                "amount": float,           // Amount of money to set aside or invest (e.g., 500.00)
                "due_date": "YYYY-MM-DD",  // Target date for completing the step (e.g., "2024-12-31")
                "status": bool             // Status: true if completed, false if not
            }},
            ...
        ]
        ```

        ### Additional Requirements:
        - Include **at least five** steps in the plan.
        - Ensure that the steps are based on the user's **income, expenses, debts, financial goals**, and the timeframe they have for these goals.
        - The plan must be divided into both **short-term** (e.g., building an emergency fund, paying off credit card debt) and **long-term** strategies (e.g., saving for retirement, investing in a diversified portfolio).
        - Consider the user’s **risk tolerance** when providing investment options (e.g., stocks, bonds, real estate).
        - Provide clear target dates to help the user track progress.

        Your response should be structured **only in JSON format**.
    """

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