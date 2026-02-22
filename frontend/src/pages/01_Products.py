import streamlit as st
from services.api import api_client
from src.components.product_display import display_products
from config import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG)
st.title("🛍️ Browse Products")

# Search and filter
col1, col2 = st.columns([3, 1])

with col1:
    search_query = st.text_input("Search products...", placeholder="Enter product name")

with col2:
    category = st.selectbox("Filter by category", ["All", "Electronics", "Clothing", "Books", "Home"])

# Pagination
page = st.number_input("Page", min_value=1, value=1)
limit = st.selectbox("Items per page", [5, 10, 20])

# Fetch products
try:
    if search_query:
        response = api_client.search_products(search_query, page=page, limit=limit)
    else:
        cat_param = None if category == "All" else category
        response = api_client.get_products(page=page, limit=limit, category=cat_param)
    
    if response.get("success", True):
        products = response.get("products", response.get("data", []))
        pagination = response.get("pagination", {})
        
        st.write(f"Found **{pagination.get('total_items', len(products))}** products")
        
        display_products(products, columns=3)
        
        # Pagination info
        col1, col2, col3 = st.columns(3)
        with col2:
            st.write(f"Page {pagination.get('current_page', page)} of {pagination.get('total_pages', 1)}")
    else:
        st.error(response.get("message", "Failed to fetch products"))

except Exception as e:
    st.error(f"Error fetching products: {str(e)}")
