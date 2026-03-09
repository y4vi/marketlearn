from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# On Streamlit Cloud, secrets are stored via st.secrets
try:
    import streamlit as st
    if not OPENAI_API_KEY:
        OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")
    if not NEWS_API_KEY:
        NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")
except Exception:
    pass