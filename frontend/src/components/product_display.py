import streamlit as st
from services.api import api_client

def display_products(products: list, columns: int = 3):
    """Display products in a grid"""
    if not products:
        st.info("No products found")
        return

    cols = st.columns(columns)
    for idx, product in enumerate(products):
        with cols[idx % columns]:
            st.subheader(product["name"])
            
            if product.get("image_url"):
                st.image(product["image_url"], use_column_width=True)
            
            st.write(f"**Price:** ${product['price']:.2f}")
            st.write(f"**Stock:** {product['stock']} units")
            
            if product.get("category"):
                st.badge(product["category"], "primary")
            
            if product.get("description"):
                st.write(product["description"][:100] + "..." if len(product["description"]) > 100 else product["description"])
            
            st.divider()

def display_cart(cart_items: list):
    """Display shopping cart"""
    if not cart_items:
        st.info("Your cart is empty")
        return

    total = 0
    for item in cart_items:
        st.write(f"**{item['name']}** x{item['quantity']} = ${item['total']:.2f}")
        total += item["total"]

    st.divider()
    st.write(f"**Total:** ${total:.2f}")

def display_order(order: dict):
    """Display order details"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Order ID:** {order['id']}")
        st.write(f"**Status:** {order['status']}")
        st.write(f"**Total:** ${order['total_amount']:.2f}")
    
    with col2:
        st.write(f"**Address:** {order['shipping_address']}")
        st.write(f"**Date:** {order.get('created_at', 'N/A')}")
