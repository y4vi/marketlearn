from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY") or os.getenv("NEWS_API_KEY")