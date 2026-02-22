import streamlit as st
from config import PAGE_CONFIG, APP_NAME, APP_ICON

# Page config
st.set_page_config(**PAGE_CONFIG)

# Title
st.title(f"{APP_ICON} {APP_NAME}")

st.markdown("""
---
## Welcome to Our E-Commerce Store!

**Features:**
- 🛒 Browse thousands of products
- 🔐 Secure authentication with JWT
- 📦 Track your orders in real-time
- ⚙️ Admin dashboard for management

---

### Quick Navigation

Use the sidebar to navigate:
- **🏠 Home** - Login/Register
- **🛍️ Products** - Browse and search
- **📦 Orders** - Track your orders
- **⚙️ Admin** - Manage store (admin only)

---
""")

st.sidebar.info("""
**About This Store**

A modern e-commerce platform built with:
- **Backend:** FastAPI + MySQL
- **Frontend:** Streamlit
- **Architecture:** Modular & Scalable

For more information, see README.md files.
""")
