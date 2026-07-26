"""Groq API client wrapper."""

import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from project root .env
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)


def get_groq_api_key() -> str:
    """Retrieve Groq API key checking Streamlit secrets first, then environment."""
    try:
        import streamlit as st
        if "GROQ_API_KEY" in st.secrets and str(st.secrets["GROQ_API_KEY"]).strip():
            return str(st.secrets["GROQ_API_KEY"]).strip()
    except Exception:
        pass

    load_dotenv(dotenv_path=_ENV_PATH, override=True)
    val = os.getenv("GROQ_API_KEY", "")
    if not val:
        load_dotenv(dotenv_path=Path.cwd() / ".env", override=True)
        val = os.getenv("GROQ_API_KEY", "")
    return val.strip()


def call_groq(prompt: str, model: str = "llama-3.1-8b-instant", system: str = None) -> str:
    """Call Groq API with prompt and optional system instructions.
    
    Args:
        prompt: User input prompt string.
        model: Groq model name (default: 'llama-3.1-8b-instant').
        system: System instruction prompt string.
        
    Returns:
        String response from the LLM or error message.
    """
    api_key = get_groq_api_key()
    if not api_key:
        print("[Warning] GROQ_API_KEY is not set in environment or .env file.")
        return "[Groq Error] GROQ_API_KEY is missing. Please configure it in your .env file or Streamlit Secrets."

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
