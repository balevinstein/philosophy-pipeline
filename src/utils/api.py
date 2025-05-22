# src/utils/api.py
from typing import Dict, Any, Optional, Callable
import os
import logging
import base64
from pathlib import Path
import openai
import anthropic
import yaml
from dotenv import load_dotenv
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    wait_random,
    retry_if_exception_type,
    RetryCallState,
)
import time


def create_retry_decorator(
    max_attempts: int = 5, min_wait: int = 4, max_wait: int = 60
) -> Callable:
    """Create a retry decorator with custom settings"""

    def before_sleep_handler(retry_state: RetryCallState):
        """Handle logging before sleep"""
        exception = retry_state.outcome.exception()
        if isinstance(exception, anthropic.RateLimitError):
            print(
                f"\nRate limit hit, waiting {retry_state.next_action.sleep} seconds..."
            )
        else:
            print(f"\nAPI error: {str(exception)}")
            print(f"Retrying in {retry_state.next_action.sleep} seconds...")

    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=2, min=min_wait, max=max_wait)
        + wait_random(0, 2),  # Add jitter
        retry=retry_if_exception_type(
            (
                anthropic.RateLimitError,  # Handle rate limits
                anthropic.APIError,  # Handle API errors
                anthropic.APIConnectionError,  # Handle connection issues
                Exception,  # Handle unexpected errors
            )
        ),
        before_sleep=before_sleep_handler,
    )


def load_config() -> Dict[str, Any]:
    """Load configuration from yaml file"""
    with open("config/conceptual_config.yaml", "r") as f:
        return yaml.safe_load(f)


class APIHandler:
    def __init__(self, config: Dict[str, Any] = None):
        load_dotenv()
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")

        if not self.openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        if not self.anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.openai_client = openai.OpenAI(api_key=self.openai_key)
        # In APIHandler.__init__
        self.anthropic_client = anthropic.Client(
            api_key=self.anthropic_key,
            # Add any required headers through client configuration
            default_headers={"anthropic-beta": "pdfs-2024-09-25"},
        )
        if config is None:
            self.config = self.load_config()  # Load default if none provided
        else:
            self.config = config
        self.o1_calls = 0

        self.logger = logging.getLogger(__name__)

        self._retry_with_rate_limit = create_retry_decorator(
            max_attempts=5, min_wait=4, max_wait=60
        )

        self._retry_standard = create_retry_decorator(
            max_attempts=3, min_wait=2, max_wait=30
        )

    # To make loading the config easier in the run_phase_one script.
    # Check there are no problems when loading a different config for tests.
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from yaml file"""
        with open("config/conceptual_config.yaml", "r") as f:
            return yaml.safe_load(f)

    def _encode_pdf(self, pdf_path: Path) -> str:
        """Convert PDF to base64 encoding"""
        with open(pdf_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")

    def _call_anthropic_with_pdf(
        self, prompt: str, pdf_path: Path, config: Dict[str, Any]
    ) -> str:
        """Make Anthropic API call with PDF support"""

        @self._retry_with_rate_limit
        def make_call():
            try:
                # Encode PDF
                pdf_data = self._encode_pdf(pdf_path)

                # Construct message content
                content = [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data,
                        },
                    },
                    {"type": "text", "text": prompt},
                ]

                # Make API call
                response = self.anthropic_client.messages.create(
                    model=config["model"],
                    max_tokens=config["max_tokens"],
                    messages=[{"role": "user", "content": content}],
                    # Headers will be handled by the client configuration
                )
                return response.content[0].text

            except Exception as e:
                print(f"Anthropic API call with PDF failed: {e}")
                raise

        return make_call()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception, openai.APIError)),
    )
    def _call_openai(self, prompt: str, config: Dict[str, Any]) -> str:
        """Make OpenAI API call with retries"""
        try:
            print(f"\nMaking API call to {config['model']}")

            # Track o1 usage
            if "o1" in config["model"]:
                self.o1_calls += 1
                print(f"o1 calls this session: {self.o1_calls}")

            # For o1 models
            if "o1" in config["model"]:
                messages = [{"role": "user", "content": prompt}]
                response = self.openai_client.chat.completions.create(
                    model=config["model"],
                    messages=messages,
                    temperature=1,  # TODO: This should probably not that high
                )
                content = response.choices[0].message.content
                if not content.strip():  # If empty response
                    print("Received empty response, retrying...")
                    raise Exception("Empty response from API")
                return content

            # For other OpenAI models
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
            response = self.openai_client.chat.completions.create(
                model=config["model"],
                messages=messages,
                max_tokens=config["max_tokens"],
                temperature=config["temperature"],
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"\nAPI call failed: {str(e)}")
            print(f"Model: {config['model']}")
            print(f"Config: {config}")
            raise

    def _call_anthropic(self, prompt: str, config: Dict[str, Any]) -> str:
        """Make standard Anthropic API call"""

        @self._retry_standard  # Use standard retry for normal calls
        def make_call():
            """Make Anthropic API call without PDF"""
            try:
                print(f"\nMaking API call to {config['model']}")

                # Add a delay between retries to avoid rate limits
                time.sleep(1)

                # Try with a smaller max_tokens if we're getting errors
                max_tokens = config["max_tokens"]

                # Try with a smaller prompt if needed
                current_prompt = prompt

                response = self.anthropic_client.messages.create(
                    model=config["model"],
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": current_prompt}],
                )
                return response.content[0].text
            except anthropic.InternalServerError as e:
                print(f"Anthropic Internal Server Error: {e}")
                print("This is likely a temporary issue with the Anthropic API.")
                print("Retrying with a shorter prompt and fewer tokens...")

                # Try with a much smaller prompt and fewer tokens
                shortened_prompt = prompt[:20000] if len(prompt) > 20000 else prompt
                try:
                    response = self.anthropic_client.messages.create(
                        model=config["model"],
                        max_tokens=min(config["max_tokens"], 4000),
                        messages=[{"role": "user", "content": shortened_prompt}],
                    )
                    return response.content[0].text
                except Exception as inner_e:
                    print(f"Still failed with shortened prompt: {inner_e}")
                    raise
            except Exception as e:
                print(f"Anthropic API call failed: {e}")
                raise

        return make_call()

    def make_api_call(
        self, stage: str, prompt: str, pdf_path: Optional[Path] = None
    ) -> str:
        """Make API call to appropriate provider based on stage"""
        model_config = self.config["models"][stage]

        if model_config["provider"] == "openai":
            return self._call_openai(prompt, model_config)
        elif model_config["provider"] == "anthropic":
            if pdf_path:
                return self._call_anthropic_with_pdf(prompt, pdf_path, model_config)
            return self._call_anthropic(prompt, model_config)
        else:
            raise ValueError(f"Unknown provider: {model_config['provider']}")
