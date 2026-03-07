"""Simple agent implementation using the OpenAI Python client.

This avoids a fragile dependency on a specific LangChain import and
works cross-platform (macOS, Linux, Windows) as long as the
`OPENAI_API_KEY` is provided in `config/settings.py` or the environment.
"""

from openai import OpenAI
import os
from typing import Optional
from ai.ai.prompts import SYSTEM_PROMPT
from config.settings import OPENAI_API_KEY

# Do not raise at import time — delay checking until the agent is invoked.
_KEY = OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY")
_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

client = None
if _KEY:
    client = OpenAI(api_key=_KEY)

class SimpleAgent:
    def __init__(self, model: Optional[str] = None, temperature: float = 0.2):
        self.model = model or _MODEL
        self.temperature = temperature

    def invoke(self, input_dict):
        key = _KEY or os.environ.get('OPENAI_API_KEY')
        if not key:
            raise ValueError("OPENAI_API_KEY not found in environment or config/settings.py")

        # Ensure client exists (lazy create if needed)
        global client
        if client is None:
            client = OpenAI(api_key=key)

        user_input = input_dict.get("input", "")
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ]

        resp = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=800,
        )

        # v1 client returns choices with message object
        content = None
        try:
            content = resp.choices[0].message.content
        except Exception:
            # Fallback to older-style mapping
            try:
                content = resp['choices'][0]['message']['content']
            except Exception:
                content = str(resp)

        return {"output": content}


agent = SimpleAgent()