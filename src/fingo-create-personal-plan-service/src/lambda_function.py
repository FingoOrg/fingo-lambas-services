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
        You are a financial expert tasked with creating a detailed and personalized financial plan for the user. The user has provided comprehensive information regarding their financial situation, including income, expenses, debts, financial goals, risk tolerance, and plans for the future.

        Below is a summary of the user's financial profile based on their responses:

        {form_data}

        Your task is to generate a **step-by-step personal financial and investment plan** for the user, focusing on both savings and investment strategies. Each step should be clear and actionable, with the following structure:

        **Step Structure**:
        - **id**: A unique identifier for the step.
        - **title**: A concise title summarizing the step.
        - **description**: A brief explanation of what needs to be done in this step and why it’s important.
        - **type**: The type of step, which can be either "investment" or "savings".
        - **amount**: The amount of money to be set aside or invested in this step.
        - **due_date**: A target date for completing the step. The planning should consider the user's financial goals and the timeframes provided in the form_data.
        - **status**: A boolean value (`true` or `false`) indicating whether the step has been completed or not.

        ### Key Deliverables for the Plan:

        1. **Analysis of Current Financial Health**: Provide an assessment of the user's financial situation, highlighting strengths and weaknesses.
        2. **Income and Expense Management**: Include actionable steps to manage income and expenses, focusing on increasing savings and reducing unnecessary expenditures.
        3. **Debt Management Plan**: Steps to manage and prioritize debt repayment, especially for high-interest debts like credit cards.
        4. **Savings Plan for Short-Term Goals**: A personalized savings plan to help the user meet short-term goals, such as vacations and purchasing a new computer.
        5. **Investment and Savings Strategy for Long-Term Goals**: A step-by-step strategy for investing and saving for long-term goals, including home ownership and retirement. This strategy should account for the user's moderate risk tolerance and planned retirement at 65 years old.
        6. **Emergency Fund Evaluation**: Steps to evaluate and potentially increase the user's emergency fund, which currently covers three months of expenses.
        7. **Entrepreneurial and Career Goals**: Provide steps on how the user can financially prepare for starting a business while maintaining career progress.
        8. **Additional Recommendations**: Offer any other financial advice that would help the user based on their situation.

        ### Example Step:

        - **id**: 1
        - **title**: Build an emergency fund for six months of expenses
        - **description**: The user should focus on increasing their emergency fund to cover six months of essential expenses in case of job loss or unexpected events.
        - **type**: Savings
        - **amount**: $5,000 (this amount should be calculated based on the user’s monthly expenses)
        - **due_date**: December 2024 (this should be adjusted according to the user's financial goals and current savings rate)
        - **status**: false

        Ensure that each step is realistic, taking into account the user's income, expenses, and goals. Provide **at least five steps**, ensuring a balance between savings and investment strategies, and tailor the timeline to help the user achieve both their short-term and long-term financial goals.

        Please structure your response clearly and in a way that the steps can be easily parsed and followed by the user. Ensure each step has all the required fields (id, title, description, type, amount, due_date, status).
    """

    print(f"LLM Query: {format_form_data(form_data)}")

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