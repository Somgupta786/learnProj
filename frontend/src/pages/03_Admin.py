import streamlit as st
from services.api import api_client
from src.utils.auth import is_authenticated, get_current_user
from config import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG)
st.title("⚙️ Admin Panel")

if not is_authenticated():
    st.warning("Please login to access admin panel")
elif get_current_user().get("role") != "admin":
    st.error("You don't have admin access")
else:
    tab1, tab2, tab3 = st.tabs(["Manage Products", "Manage Orders", "Dashboard"])
    
    # Tab 1: Manage Products
    with tab1:
        st.subheader("Products Management")
        
        action = st.radio("Action", ["View", "Create", "Edit", "Delete"])
        
        if action == "View":
            response = api_client.get_products(limit=50)
            products = response.get("products", response.get("data", []))
            st.dataframe(products)
        
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
                response = api_client.create_product(product_data)
                if response.get("id"):
                    st.success("Product created successfully!")
                else:
                    st.error(response.get("detail", "Failed to create product"))
        
        elif action == "Edit":
            product_id = st.number_input("Product ID", min_value=1)
            if st.button("Load Product"):
                product = api_client.get_product(product_id)
                if product:
                    st.session_state.product = product
            
            if "product" in st.session_state:
                product = st.session_state.product
                name = st.text_input("Product Name", value=product.get("name", ""))
                price = st.number_input("Price", value=product.get("price", 0))
                stock = st.number_input("Stock", value=product.get("stock", 0), step=1)
                
                if st.button("Update Product"):
                    update_data = {"name": name, "price": price, "stock": stock}
                    response = api_client.update_product(product_id, update_data)
                    if response.get("id"):
                        st.success("Product updated!")
                    else:
                        st.error("Update failed")
        
        elif action == "Delete":
            product_id = st.number_input("Product ID to delete", min_value=1)
            if st.button("Delete Product", type="secondary"):
                response = api_client.delete_product(product_id)
                st.success("Product deleted!")
    
    # Tab 2: Manage Orders
    with tab2:
        st.subheader("Orders Management")
        
        page = st.number_input("Page", min_value=1, value=1, key="orders_page")
        response = api_client.get_all_orders(page=page, limit=10)
        
        orders = response.get("orders", response.get("data", []))
        
        if orders:
            for order in orders:
                with st.expander(f"Order #{order['id']} - User #{order['user_id']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Amount:** ${order['total_amount']:.2f}")
                        st.write(f"**Status:** {order['status']}")
                    
                    with col2:
                        new_status = st.selectbox(
                            "Update Status",
                            ["pending", "processing", "shipped", "delivered", "cancelled"],
                            key=f"status_{order['id']}"
                        )
                        if st.button("Update", key=f"btn_{order['id']}"):
                            api_client.update_order_status(order['id'], new_status)
                            st.success("Status updated!")
        else:
            st.info("No orders found")
    
    # Tab 3: Dashboard
    with tab3:
        st.subheader("Dashboard")
        st.write("Admin Dashboard Stats")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Products", "Loading...", "")
        
        with col2:
            st.metric("Total Orders", "Loading...", "")
        
        with col3:
            st.metric("Total Users", "Loading...", "")
