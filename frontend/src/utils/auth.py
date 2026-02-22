import streamlit as st
from services.api import api_client

def authenticate():
    """Authentication management"""
    if "user" not in st.session_state:
        st.session_state.user = None
    if "token" not in st.session_state:
        st.session_state.token = None

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.user is not None

def get_current_user():
    """Get current user"""
    return st.session_state.user

def get_auth_header() -> dict:
    """Get authorization header"""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def login_user(email: str, password: str) -> bool:
    """Login user"""
    try:
        response = api_client.login(email, password)
        if response.get("access_token"):
            st.session_state.token = response["access_token"]
            st.session_state.user = response.get("user", {})
            api_client.set_token(response["access_token"])
            return True
        return False
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False

def logout_user():
    """Logout user"""
    st.session_state.user = None
    st.session_state.token = None
    api_client.set_token(None)

def register_user(name: str, email: str, password: str, phone: str = None) -> bool:
    """Register new user"""
    try:
        response = api_client.register(name, email, password, phone)
        if response.get("id"):
            return True
        return False
    except Exception as e:
        st.error(f"Registration error: {str(e)}")
        return False
