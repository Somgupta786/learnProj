import streamlit as st
import requests

st.set_page_config(page_title="E-Commerce Store", page_icon="🛒", layout="wide")
st.title("🛍️ Browse Products")

API_URL = "http://localhost:8000/api"

# Initialize session
if "user" not in st.session_state:
    st.session_state.user = None

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
        params = {"q": search_query, "page": page, "limit": limit}
        response = requests.get(f"{API_URL}/products/search", params=params)
    else:
        params = {"page": page, "limit": limit}
        if category != "All":
            params["category"] = category
        response = requests.get(f"{API_URL}/products", params=params)
    
    if response.status_code == 200:
        data = response.json()
        products = data.get("products", data.get("data", []))
        pagination = data.get("pagination", {})
        
        st.write(f"Found **{pagination.get('total_items', len(products))}** products")
        
        if products:
            cols = st.columns(3)
            for idx, product in enumerate(products):
                with cols[idx % 3]:
                    st.subheader(product["name"])
                    
                    if product.get("image_url"):
                        st.image(product["image_url"], use_column_width=True)
                    
                    st.write(f"**Price:** ${product['price']:.2f}")
                    st.write(f"**Stock:** {product['stock']} units")
                    
                    if product.get("category"):
                        st.caption(product["category"])
                    
                    if product.get("description"):
                        desc = product["description"]
                        st.write(desc[:100] + "..." if len(desc) > 100 else desc)
                    
                    st.divider()
        else:
            st.info("No products found")
        
        # Pagination info
        col1, col2, col3 = st.columns(3)
        with col2:
            st.write(f"Page {pagination.get('current_page', page)} of {pagination.get('total_pages', 1)}")
    else:
        st.error("Failed to fetch products")

except Exception as e:
    st.error(f"Error fetching products: {str(e)}")

