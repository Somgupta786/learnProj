import streamlit as st
from services.api import api_client
from src.utils.auth import is_authenticated
from config import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG)
st.title("📦 Your Orders")

if not is_authenticated():
    st.warning("Please login to view your orders")
else:
    try:
        page = st.number_input("Page", min_value=1, value=1)
        limit = st.selectbox("Orders per page", [5, 10, 20])
        
        response = api_client.get_user_orders(page=page, limit=limit)
        
        if response.get("success", True):
            orders = response.get("orders", response.get("data", []))
            pagination = response.get("pagination", {})
            
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
            st.error(response.get("message", "Failed to fetch orders"))
    
    except Exception as e:
        st.error(f"Error fetching orders: {str(e)}")
