import streamlit as st
import requests

st.set_page_config(page_title="E-Commerce Store", page_icon="🛒", layout="wide")
st.title("📦 Your Orders")

API_URL = "http://localhost:8000/api"

# Initialize session
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None

is_authenticated = st.session_state.user is not None

if not is_authenticated:
    st.warning("Please login to view your orders")
else:
    try:
        page = st.number_input("Page", min_value=1, value=1)
        limit = st.selectbox("Orders per page", [5, 10, 20])
        
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        params = {"page": page, "limit": limit}
        response = requests.get(f"{API_URL}/orders", params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            orders = data.get("orders", data.get("data", []))
            pagination = data.get("pagination", {})
            
            if not orders:
                st.info("You haven't placed any orders yet")
            else:
                st.write(f"You have **{pagination.get('total_items', len(orders))}** orders")
                
                for order in orders:
                    with st.expander(f"Order #{order['id']} - {order['status'].upper()}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Total:** ${order['total_amount']:.2f}")
                            st.write(f"**Status:** {order['status']}")
                        
                        with col2:
                            st.write(f"**Address:** {order['shipping_address']}")
                            st.write(f"**Date:** {order.get('created_at', 'N/A')}")
        else:
            st.error("Failed to fetch orders")
    
    except Exception as e:
        st.error(f"Error fetching orders: {str(e)}")

