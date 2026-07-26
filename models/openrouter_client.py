"""OpenRouter API client wrapper using OpenAI SDK."""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


def call_openrouter(prompt: str, model: str = "openai/gpt-4o-mini", system: str = None) -> str:
    """Call OpenRouter API with prompt and optional system instructions.
    
    Args:
        prompt: User input prompt string.
        model: OpenRouter model identifier (default: 'openai/gpt-4o-mini').
        system: System instruction prompt string.
        
    Returns:
        String response from the LLM or error message.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("[Warning] OPENROUTER_API_KEY is not set in environment or .env file.")
        return "[OpenRouter Error] OPENROUTER_API_KEY is missing. Please configure it in your .env file."

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[OpenRouter API Failure]: {e}")
        return f"[OpenRouter Error] API call failed: {str(e)}"
