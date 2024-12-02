# src/utils/api.py
import os
import openai
import anthropic
from typing import Dict, Any
import yaml
from dotenv import load_dotenv
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type  # Added import


def load_config() -> Dict[str, Any]:
    """Load configuration from yaml file"""
    with open("config/config.yaml", 'r') as f:
        return yaml.safe_load(f)

class APIHandler:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Get API keys
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Verify keys are present
        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        if not self.anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            
        # Initialize clients
        self.openai_client = openai.OpenAI(api_key=self.openai_key)
        self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
        
        # Load config
        self.config = load_config()
        
        # Track o1 usage
        self.o1_calls = 0

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception, openai.APIError))
    )
    def _call_openai(self, prompt: str, config: Dict[str, Any]) -> str:
        """Make OpenAI API call with retries"""
        try:
            print(f"\nMaking API call to {config['model']}")
            
            # Track o1 usage
            if 'o1' in config['model']:
                self.o1_calls += 1
                print(f"o1 calls this session: {self.o1_calls}")
            
            # For o1 models
            if 'o1' in config['model']:
                messages = [{"role": "user", "content": prompt}]
                response = self.openai_client.chat.completions.create(
                    model=config['model'],
                    messages=messages,
                    max_completion_tokens=config['max_tokens'],
                    temperature=1
                )
                content = response.choices[0].message.content
                if not content.strip():  # If empty response
                    print("Received empty response, retrying...")
                    raise Exception("Empty response from API")
                return content
                
            # For other OpenAI models
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
            response = self.openai_client.chat.completions.create(
                model=config['model'],
                messages=messages,
                max_tokens=config['max_tokens'],
                temperature=config['temperature']
            )
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"\nAPI call failed: {str(e)}")
            print(f"Model: {config['model']}")
            print(f"Config: {config}")
            raise

    def _call_anthropic(self, prompt: str, config: Dict[str, Any]) -> str:
        """Make Anthropic API call"""
        try:
            response = self.anthropic_client.messages.create(
                model=config['model'],
                max_tokens=config['max_tokens'],
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Anthropic API call failed: {e}")
            raise

    def make_api_call(self, stage: str, prompt: str) -> str:
        """Make API call to appropriate provider based on stage"""
        model_config = self.config['models'][stage]
        
        if model_config['provider'] == 'openai':
            return self._call_openai(prompt, model_config)
        elif model_config['provider'] == 'anthropic':
            return self._call_anthropic(prompt, model_config)
        else:
            raise ValueError(f"Unknown provider: {model_config['provider']}")