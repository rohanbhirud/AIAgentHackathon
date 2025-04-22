import os
import json
import re
from dotenv import load_dotenv
from openai import AzureOpenAI
from typing import Dict, Any, Optional

# Load environment variables
load_dotenv()

class AzureAIClient:
    """Client for interacting with Azure OpenAI services"""
    
    def __init__(self) -> None:
        """Initialize the Azure OpenAI client"""
        # Load configuration from environment variables
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.client = None
        
        # Initialize Azure OpenAI client
        try:
            # Check for required parameters
            if not all([self.api_key, self.endpoint]):
                print("❌ Azure OpenAI configuration missing from environment variables")
                print(f"   API Key: {'✅' if self.api_key else '❌'}")
                print(f"   Endpoint: {'✅' if self.endpoint else '❌'}")
                return
                
            # Initialize the OpenAI client
            self.client = AzureOpenAI(
                api_version=self.api_version,
                azure_endpoint=self.endpoint,
                api_key=self.api_key,
            )
            
            print(f"✅ Azure OpenAI client initialized with deployment: {self.deployment}")
        except Exception as e:
            print(f"❌ Failed to initialize Azure OpenAI client: {e}")
            self.client = None