import streamlit as st
import requests
import sys
import os

# Get parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    from config import PAGE_CONFIG, APP_NAME, APP_ICON
    from utils.auth import authenticate, is_authenticated, login_user, logout_user, register_user
except ImportError:
    # Fallback if imports fail
    PAGE_CONFIG = {
        "page_title": "E-Commerce Store",
        "page_icon": "🛒",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
    APP_NAME = "E-Commerce Store"
    APP_ICON = "🛒"

# Page config
st.set_page_config(**PAGE_CONFIG)

# Initialize auth if function exists
try:
    authenticate()
except:
    if "user" not in st.session_state:
        st.session_state.user = None
    if "token" not in st.session_state:
        st.session_state.token = None

def is_auth():
    return st.session_state.user is not None

# Sidebar
with st.sidebar:
    st.title(f"{APP_ICON} {APP_NAME}")
    
    if is_auth():
        user = st.session_state.user
        st.write(f"Welcome, **{user.get('name', 'User')}**!")
        st.write(f"Email: {user.get('email')}")
        
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.token = None
            st.rerun()
    else:
        st.write("Please login or register to continue")

# Main content
st.title(f"{APP_ICON} Welcome to {APP_NAME}")

if not is_auth():
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    API_URL = "http://localhost:8000/api"
    
    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if email and password:
                try:
                    response = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.token = data.get("access_token")
                        st.session_state.user = data.get("user", {})
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                except Exception as e:
                    st.error(f"Login error: {str(e)}")
            else:
                st.error("Please enter email and password")
    
    with tab2:
        st.subheader("Register")
        name = st.text_input("Full Name", key="register_name")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        phone = st.text_input("Phone", key="register_phone")
        
        if st.button("Register"):
            if name and email and password:
                try:
                    data = {"name": name, "email": email, "password": password, "phone": phone}
                    response = requests.post(f"{API_URL}/auth/register", json=data)
                    if response.status_code == 201:
                        st.success("Registration successful! Please login.")
                    else:
                        st.error(response.json().get("detail", "Registration failed"))
                except Exception as e:
                    st.error(f"Registration error: {str(e)}")
            else:
                st.error("Please fill all required fields")
else:
    st.success("You are logged in!")
    st.write("Navigate to different pages using the sidebar menu.")

