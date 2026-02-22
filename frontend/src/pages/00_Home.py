import streamlit as st
from src.utils.auth import authenticate, is_authenticated, login_user, logout_user, register_user
from config import PAGE_CONFIG, APP_NAME, APP_ICON

# Page config
st.set_page_config(**PAGE_CONFIG)

# Initialize auth
authenticate()

# Sidebar
with st.sidebar:
    st.title(f"{APP_ICON} {APP_NAME}")
    
    if is_authenticated():
        user = st.session_state.user
        st.write(f"Welcome, **{user.get('name', 'User')}**!")
        st.write(f"Email: {user.get('email')}")
        
        if st.button("Logout"):
            logout_user()
            st.rerun()
    else:
        st.write("Please login or register to continue")

# Main content
st.title(f"{APP_ICON} Welcome to {APP_NAME}")

if not is_authenticated():
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if email and password:
                if login_user(email, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
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
                if register_user(name, email, password, phone):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Registration failed")
            else:
                st.error("Please fill all required fields")
else:
    st.success("You are logged in!")
    st.write("Navigate to different pages using the sidebar menu.")
