import streamlit as st
import requests

st.set_page_config(page_title="E-Commerce Store", page_icon="🛒", layout="wide")
st.title("🛍️ Browse Products")

API_URL = "http://localhost:8000/api"

# Initialize session
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None
if "cart" not in st.session_state:
    st.session_state.cart = {}

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
                        try:
                            st.image(product["image_url"], use_column_width=True)
                        except:
                            st.info("📷 Image not available")
                    else:
                        st.info("📷 No image")
                    
                    st.write(f"**Price:** ${product['price']:.2f}")
                    st.write(f"**Stock:** {product['stock']} units")
                    
                    if product.get("category"):
                        st.caption(f"📁 {product['category']}")
                    
                    if product.get("description"):
                        desc = product["description"]
                        st.write(desc[:100] + "..." if len(desc) > 100 else desc)
                    
                    # Order/Cart functionality
                    if st.session_state.user:
                        col_qty, col_btn = st.columns([2, 3])
                        with col_qty:
                            qty = st.number_input("Qty", min_value=1, max_value=product['stock'], value=1, key=f"qty_{product['id']}")
                        with col_btn:
                            if st.button("🛒 Add to Cart", key=f"add_{product['id']}"):
                                st.session_state.cart[product['id']] = {
                                    "product_id": product['id'],
                                    "name": product["name"],
                                    "price": product['price'],
                                    "quantity": qty
                                }
                                st.success(f"Added {qty}x {product['name']} to cart!")
                    else:
                        st.info("Login to order")
                    
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

# Shopping Cart Section
st.divider()
st.subheader("🛒 Shopping Cart")

if st.session_state.user:
    if st.session_state.cart:
        st.write(f"Items in cart: **{len(st.session_state.cart)}**")
        
        total_amount = 0
        cart_items = []
        
        for product_id, item in st.session_state.cart.items():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"{item['name']}")
            with col2:
                st.write(f"${item['price']:.2f}")
            with col3:
                st.write(f"x{item['quantity']}")
            with col4:
                if st.button("Remove", key=f"remove_{product_id}"):
                    del st.session_state.cart[product_id]
                    st.rerun()
            
            total_amount += item['price'] * item['quantity']
            cart_items.append({
                "product_id": item['product_id'],
                "quantity": item['quantity']
            })
        
        st.write("---")
        st.write(f"**Total Amount:** ${total_amount:.2f}")
        
        # Checkout form
        shipping_address = st.text_area("Shipping Address", placeholder="Enter your address")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ Place Order", use_container_width=True):
                if shipping_address:
                    try:
                        headers = {"Authorization": f"Bearer {st.session_state.token}"}
                        order_data = {
                            "items": cart_items,
                            "total_amount": total_amount,
                            "shipping_address": shipping_address
                        }
                        response = requests.post(
                            f"{API_URL}/orders/",
                            json=order_data,
                            headers=headers,
                            timeout=10
                        )
                        
                        if response.status_code == 201:
                            st.success("✅ Order placed successfully!")
                            st.session_state.cart = {}
                            st.info(f"Order ID: {response.json().get('id')}")
                            st.rerun()
                        else:
                            st.error(f"Order failed: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error placing order: {str(e)}")
                else:
                    st.error("Please enter shipping address")
        
        with col2:
            if st.button("🗑️ Clear Cart", use_container_width=True):
                st.session_state.cart = {}
                st.rerun()
    else:
        st.info("Cart is empty. Add products to order!")
else:
    st.warning("Please login to place orders")


