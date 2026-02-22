import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="E-Commerce Store", page_icon="🛒", layout="wide")
st.title("⚙️ Admin Panel")

API_URL = "http://localhost:8000/api"

# Initialize session
if "user" not in st.session_state:
    st.session_state.user = None
if "token" not in st.session_state:
    st.session_state.token = None

is_authenticated = st.session_state.user is not None
is_admin = is_authenticated and st.session_state.user.get("role") == "admin"

if not is_authenticated:
    st.warning("Please login to access admin panel")
elif not is_admin:
    st.error("You don't have admin access")
else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    
    tab1, tab2, tab3 = st.tabs(["Manage Products", "Manage Orders", "Dashboard"])
    
    # Tab 1: Manage Products
    with tab1:
        st.subheader("Products Management")
        
        action = st.radio("Action", ["View", "Create", "Edit", "Delete"])
        
        if action == "View":
            try:
                response = requests.get(f"{API_URL}/products?limit=50", headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    products = data.get("products", data.get("data", []))
                    if products:
                        df = pd.DataFrame(products)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No products found")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        elif action == "Create":
            st.write("Create New Product")
            name = st.text_input("Product Name")
            description = st.text_area("Description")
            price = st.number_input("Price", min_value=0.01)
            stock = st.number_input("Stock", min_value=0, step=1)
            category = st.text_input("Category")
            image_url = st.text_input("Image URL")
            
            if st.button("Create Product"):
                product_data = {
                    "name": name,
                    "description": description,
                    "price": price,
                    "stock": stock,
                    "category": category,
                    "image_url": image_url
                }
                try:
                    response = requests.post(f"{API_URL}/products", json=product_data, headers=headers)
                    if response.status_code == 201:
                        st.success("Product created successfully!")
                    else:
                        st.error(response.json().get("detail", "Failed to create product"))
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        elif action == "Edit":
            product_id = st.number_input("Product ID", min_value=1)
            if st.button("Load Product"):
                try:
                    response = requests.get(f"{API_URL}/products/{product_id}", headers=headers)
                    if response.status_code == 200:
                        st.session_state.product = response.json()
                        st.success("Product loaded")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            if "product" in st.session_state:
                product = st.session_state.product
                name = st.text_input("Product Name", value=product.get("name", ""))
                price = st.number_input("Price", value=product.get("price", 0))
                stock = st.number_input("Stock", value=product.get("stock", 0), step=1)
                
                if st.button("Update Product"):
                    update_data = {"name": name, "price": price, "stock": stock}
                    try:
                        response = requests.put(f"{API_URL}/products/{product_id}", json=update_data, headers=headers)
                        if response.status_code == 200:
                            st.success("Product updated!")
                        else:
                            st.error("Update failed")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        elif action == "Delete":
            product_id = st.number_input("Product ID to delete", min_value=1)
            if st.button("Delete Product", type="secondary"):
                try:
                    response = requests.delete(f"{API_URL}/products/{product_id}", headers=headers)
                    if response.status_code == 204:
                        st.success("Product deleted!")
                    else:
                        st.error("Delete failed")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Tab 2: Manage Orders
    with tab2:
        st.subheader("Orders Management")
        
        page = st.number_input("Page", min_value=1, value=1, key="orders_page")
        
        try:
            params = {"page": page, "limit": 10}
            response = requests.get(f"{API_URL}/orders/admin/all", params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                orders = data.get("orders", data.get("data", []))
                
                if orders:
                    for order in orders:
                        with st.expander(f"Order #{order['id']} - User #{order['user_id']}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Amount:** ${order['total_amount']:.2f}")
                                st.write(f"**Current Status:** {order['status']}")
                            
                            with col2:
                                new_status = st.selectbox(
                                    "Update Status",
                                    ["pending", "processing", "shipped", "delivered", "cancelled"],
                                    key=f"status_{order['id']}"
                                )
                                if st.button("Update", key=f"btn_{order['id']}"):
                                    update_data = {"status": new_status}
                                    update_response = requests.put(f"{API_URL}/orders/{order['id']}/status", json=update_data, headers=headers)
                                    if update_response.status_code == 200:
                                        st.success("Status updated!")
                                    else:
                                        st.error("Update failed")
                else:
                    st.info("No orders found")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Tab 3: Dashboard
    with tab3:
        st.subheader("Dashboard")
        
        try:
            # Get product count
            prod_response = requests.get(f"{API_URL}/products?limit=1", headers=headers)
            prod_count = prod_response.json().get("pagination", {}).get("total_items", 0) if prod_response.status_code == 200 else 0
            
            # Get order count
            order_response = requests.get(f"{API_URL}/orders/admin/all?limit=1", params={"limit": 1}, headers=headers)
            order_count = order_response.json().get("pagination", {}).get("total_items", 0) if order_response.status_code == 200 else 0
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Products", prod_count)
            
            with col2:
                st.metric("Total Orders", order_count)
            
            with col3:
                st.metric("Total Users", "N/A")
        except Exception as e:
            st.error(f"Error loading dashboard: {str(e)}")

