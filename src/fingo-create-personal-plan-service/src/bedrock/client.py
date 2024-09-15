import boto3
import json
import os
from botocore.exceptions import ClientError

class BedrockClient:
    def __init__(self, region_name, max_tokens=512, temperature=0.5, top_p=None, top_k=None, stop_sequences=None):
        self.client = boto3.client("bedrock-runtime", region_name=region_name)
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.stop_sequences = stop_sequences

    def invoke_anthropic_claude(self, model_id, prompt):
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        }

        if self.top_p is not None:
            native_request["top_p"] = self.top_p
        
        if self.top_k is not None:
            native_request["top_k"] = self.top_k
        
        if self.stop_sequences is not None:
            native_request["stop_sequences"] = self.stop_sequences

        request_payload = json.dumps(native_request)

        try:
            response = self.client.invoke_model(
                modelId=model_id,
                body=request_payload
            )
            return self._handle_response(response)
        except (ClientError, Exception) as e:
            print(f"Failed to invoke model: {e}")
            return {"error": str(e)}

    def _handle_response(self, response):
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            model_response = json.loads(response["body"].read())
            return model_response["content"][0]["text"]
        else:
            return {"error": "Failed to invoke model."}