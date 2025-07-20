import os
import boto3
from langchain_aws import ChatBedrock
from dotenv import load_dotenv

load_dotenv()


class BedrockService:
    """AWS Bedrock service wrapper for Claude models"""
    
    def __init__(self, model_id: str = None):
        """
        Initialize Bedrock service
        
        Args:
            model_id: Bedrock model ID for Claude (optional, uses env var if not provided)
                - us.anthropic.claude-3-5-sonnet-20240620-v1:0 (Claude 3.5 Sonnet)
                - us.anthropic.claude-3-haiku-20240307-v1:0 (Claude 3 Haiku)
                - us.anthropic.claude-3-sonnet-20240229-v1:0 (Claude 3 Sonnet)
        """
        self.model_id = model_id or os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-3-5-sonnet-20240620-v1:0")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        
        # Initialize boto3 client for Bedrock
        self.bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=self.region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        
        # Initialize LangChain ChatBedrock
        self.llm = ChatBedrock(
            client=self.bedrock_client,
            model_id=self.model_id,
            model_kwargs={
                "temperature": 0.1,
                "max_tokens": 4000,
            }
        )
    
    def get_llm(self):
        """Get the LangChain ChatBedrock instance"""
        return self.llm
    
    def with_structured_output(self, schema):
        """Get LLM with structured output for Pydantic models"""
        return self.llm.with_structured_output(schema)
    
    def invoke(self, messages):
        """Direct invoke method for compatibility"""
        return self.llm.invoke(messages)


# Singleton instance for easy import
bedrock_service = BedrockService()