"""
OpenRouter API Client with Extended Thinking Support

This module provides a clean interface to OpenRouter's API,
with support for Claude's extended thinking feature.
"""

import httpx
import json
import time
from typing import Optional, Dict, Any, Tuple


class OpenRouterClient:
    """
    Client for OpenRouter API with extended thinking support.
    """
    
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    # Model identifiers
    CLAUDE_SONNET = "anthropic/claude-sonnet-4-20250514"
    CLAUDE_OPUS = "anthropic/claude-opus-4-20250514"
    CLAUDE_HAIKU = "anthropic/claude-3-5-haiku"
    GPT4_TURBO = "openai/gpt-4-turbo"
    
    def __init__(
        self,
        api_key: str,
        site_url: str = "https://maxwell-processor.local",
        site_name: str = "Maxwell Treatise Processor"
    ):
        """
        Initialize the OpenRouter client.
        
        Args:
            api_key: Your OpenRouter API key
            site_url: Your site URL for ranking
            site_name: Your site name for display
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": site_url,
            "X-Title": site_name
        }
        
        # HTTP client with connection pooling
        self.client = httpx.Client(
            timeout=httpx.Timeout(300.0, connect=10.0),  # 5 min timeout
            follow_redirects=True
        )
    
    def call_with_thinking(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = CLAUDE_SONNET,
        max_tokens: int = 16000,
        thinking_budget: int = 10000,
        temperature: float = 0.3,
        retry_count: int = 3,
        retry_delay: float = 5.0
    ) -> Dict[str, Any]:
        """
        Call model with extended thinking enabled (for Claude models).
        
        Args:
            system_prompt: System message content
            user_prompt: User message content
            model: Model identifier
            max_tokens: Maximum output tokens
            thinking_budget: Token budget for extended thinking (Claude only)
            temperature: Sampling temperature
            retry_count: Number of retries on failure
            retry_delay: Delay between retries in seconds
        
        Returns:
            Full API response dictionary
        """
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            # Request JSON output if model supports it
            "response_format": {"type": "json_object"} if "gpt" in model.lower() else None
        }
        
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        # For Claude models, configure extended thinking
        if "claude" in model.lower():
            # Note: Extended thinking configuration varies by API version
            # This is the general structure - may need adjustment
            payload["provider"] = {
                "order": ["Anthropic"],
                "allow_fallbacks": False
            }
            
            # Extended thinking (if supported)
            # The exact parameter name may vary
            if thinking_budget > 0:
                # Try multiple possible parameter names
                payload["thinking"] = {
                    "type": "enabled",
                    "budget_tokens": thinking_budget
                }
        
        # Retry logic
        last_error = None
        for attempt in range(retry_count):
            try:
                response = self.client.post(
                    self.BASE_URL,
                    headers=self.headers,
                    json=payload
                )
                
                # Check for rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", retry_delay * 2))
                    print(f"  Rate limited, waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                return response.json()
                
            except httpx.TimeoutException as e:
                last_error = e
                print(f"  Timeout on attempt {attempt + 1}/{retry_count}")
                time.sleep(retry_delay)
                
            except httpx.HTTPStatusError as e:
                last_error = e
                print(f"  HTTP error {e.response.status_code}: {e.response.text[:200]}")
                if e.response.status_code >= 500:
                    time.sleep(retry_delay)
                else:
                    raise
        
        raise last_error or Exception("All retries failed")
    
    def extract_content(self, response: Dict[str, Any]) -> Tuple[str, Optional[str]]:
        """
        Extract main content and thinking from API response.
        
        Args:
            response: Full API response dictionary
        
        Returns:
            Tuple of (content, thinking_text)
            - content: The main response content
            - thinking_text: Extended thinking content (if available)
        """
        if "choices" not in response or not response["choices"]:
            raise ValueError("No choices in response")
        
        message = response["choices"][0].get("message", {})
        
        # Main content
        content = message.get("content", "")
        
        # Extended thinking (various possible locations)
        thinking = None
        
        # Try direct thinking field
        if "thinking" in message:
            thinking = message["thinking"]
        
        # Try content blocks (Claude format)
        if isinstance(message.get("content"), list):
            for block in message["content"]:
                if isinstance(block, dict):
                    if block.get("type") == "thinking":
                        thinking = block.get("thinking", "")
                    elif block.get("type") == "text":
                        content = block.get("text", content)
        
        return content, thinking
    
    def get_usage(self, response: Dict[str, Any]) -> Dict[str, int]:
        """
        Extract token usage from response.
        
        Returns dict with 'prompt_tokens', 'completion_tokens', 'total_tokens'
        """
        usage = response.get("usage", {})
        return {
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0)
        }
    
    def estimate_cost(self, response: Dict[str, Any], model: str) -> float:
        """
        Estimate cost based on token usage.
        
        Returns estimated cost in USD.
        """
        usage = self.get_usage(response)
        
        # Approximate pricing (may vary)
        pricing = {
            "anthropic/claude-sonnet-4-20250514": (3.0, 15.0),  # per 1M tokens
            "anthropic/claude-opus-4-20250514": (15.0, 75.0),
            "anthropic/claude-3-5-haiku": (0.25, 1.25),
            "openai/gpt-4-turbo": (10.0, 30.0),
        }
        
        input_rate, output_rate = pricing.get(model, (5.0, 15.0))
        
        input_cost = (usage["prompt_tokens"] / 1_000_000) * input_rate
        output_cost = (usage["completion_tokens"] / 1_000_000) * output_rate
        
        return input_cost + output_cost
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class MockOpenRouterClient:
    """
    Mock client for testing without API calls.
    """
    
    def __init__(self, response_file: str = None):
        self.response_file = response_file
        self.calls = []
    
    def call_with_thinking(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Record call and return mock response."""
        self.calls.append({
            "system": system_prompt,
            "user": user_prompt,
            "kwargs": kwargs
        })
        
        if self.response_file:
            with open(self.response_file, 'r') as f:
                return json.load(f)
        
        # Default mock response
        return {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "chapter": "MOCK_CHAPTER",
                        "articles": [],
                        "state_updates": {}
                    })
                }
            }],
            "usage": {
                "prompt_tokens": len(user_prompt) // 4,
                "completion_tokens": 100,
                "total_tokens": len(user_prompt) // 4 + 100
            }
        }
    
    def extract_content(self, response: Dict) -> Tuple[str, Optional[str]]:
        """Extract content from mock response."""
        return response["choices"][0]["message"]["content"], None


# Utility functions

def create_client(api_key: str = None, mock: bool = False) -> OpenRouterClient:
    """
    Create an OpenRouter client.
    
    Args:
        api_key: API key (uses env var if not provided)
        mock: Whether to create a mock client for testing
    
    Returns:
        OpenRouterClient or MockOpenRouterClient
    """
    if mock:
        return MockOpenRouterClient()
    
    import os
    key = api_key or os.environ.get("OPENROUTER_API_KEY")
    
    if not key:
        raise ValueError(
            "API key required. Set OPENROUTER_API_KEY environment variable "
            "or pass api_key parameter."
        )
    
    return OpenRouterClient(api_key=key)


# CLI for testing
if __name__ == "__main__":
    import os
    
    # Test with a simple prompt
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Set OPENROUTER_API_KEY to test")
    else:
        client = OpenRouterClient(api_key=api_key)
        
        response = client.call_with_thinking(
            system_prompt="You are a helpful assistant.",
            user_prompt="Say 'Hello, Maxwell!' and nothing else.",
            model=OpenRouterClient.CLAUDE_HAIKU,  # Use cheaper model for test
            max_tokens=100,
            thinking_budget=0
        )
        
        content, thinking = client.extract_content(response)
        usage = client.get_usage(response)
        
        print(f"Response: {content}")
        print(f"Tokens: {usage}")
        
        client.close()
