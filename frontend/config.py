import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Try to get API_URL from Streamlit secrets (Streamlit Cloud), then .env, then default
try:
    API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://localhost:8000/api"))
except:
    API_URL = os.getenv("API_URL", "http://localhost:8000/api")

APP_NAME = "E-Commerce Store"
APP_ICON = "🛒"

# Page config
PAGE_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": APP_ICON,
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}
