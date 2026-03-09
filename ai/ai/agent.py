"""Agent implementation using the OpenAI Python client.

Provides conversational stock analysis with automatic news context.
"""

from openai import OpenAI
import os
from typing import Optional
from ai.ai.prompts import SYSTEM_PROMPT
from config.settings import OPENAI_API_KEY

_KEY = OPENAI_API_KEY or os.environ.get("OPENAI_API_KEY")
_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

client = None
if _KEY:
    client = OpenAI(api_key=_KEY)


class SimpleAgent:
    def __init__(self, model: Optional[str] = None, temperature: float = 0.3):
        self.model = model or _MODEL
        self.temperature = temperature

    def invoke(self, input_dict):
        key = _KEY or os.environ.get('OPENAI_API_KEY')
        if not key:
            raise ValueError("OPENAI_API_KEY not found in environment or config/settings.py")

        global client
        if client is None:
            client = OpenAI(api_key=key)

        user_input = input_dict.get("input", "")
        conversation_history = input_dict.get("history", [])
        ticker = input_dict.get("ticker", "")

        # Automatically fetch recent news for real-world context
        news_context = ""
        if ticker:
            try:
                from data.news_data import fetch_news_context
                news_context = fetch_news_context(ticker)
            except Exception:
                news_context = ""

        # Build message list with full conversation history
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Append news context to the user message so the AI can reference it
        if news_context:
            user_input += f"\n\n[Recent news for context — use these to inform your analysis:]\n{news_context}"
        messages.append({"role": "user", "content": user_input})

        resp = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=1200,
        )

        try:
            content = resp.choices[0].message.content
        except Exception:
            try:
                content = resp['choices'][0]['message']['content']
            except Exception:
                content = str(resp)

        return {"output": content}


agent = SimpleAgent()