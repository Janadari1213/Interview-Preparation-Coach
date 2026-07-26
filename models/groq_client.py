"""Groq API client wrapper."""

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()


def call_groq(prompt: str, model: str = "llama-3.1-8b-instant", system: str = None) -> str:
    """Call Groq API with prompt and optional system instructions.
    
    Args:
        prompt: User input prompt string.
        model: Groq model name (default: 'llama-3.1-8b-instant').
        system: System instruction prompt string.
        
    Returns:
        String response from the LLM or error message.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("[Warning] GROQ_API_KEY is not set in environment or .env file.")
        return "[Groq Error] GROQ_API_KEY is missing. Please configure it in your .env file."

    try:
        client = Groq(api_key=api_key)
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
        print(f"[Groq API Failure]: {e}")
        return f"[Groq Error] API call failed: {str(e)}"
