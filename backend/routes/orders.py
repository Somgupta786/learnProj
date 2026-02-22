from fastapi import APIRouter, HTTPException, Depends, status, Query
from models.order import OrderCreate, OrderUpdate, OrderResponse, OrderListResponse
from db.order_db import OrderDB
from db.product_db import ProductDB
from utils.helpers import get_pagination_params, get_pagination_response
from middleware.auth import verify_token, require_admin

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, current_user = Depends(verify_token)):
    """Create a new order"""
    try:
        # Validate items and check stock
        for item in order.items:
            product = ProductDB.get_product_by_id(item.product_id)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {item.product_id} not found"
                )
            
            if product["stock"] < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for product {product['name']}"
                )
            
            # Decrease stock
            ProductDB.decrease_stock(item.product_id, item.quantity)

        # Create order
        new_order = OrderDB.create_order(
            user_id=current_user["user_id"],
            total_amount=order.total_amount,
            shipping_address=order.shipping_address
        )
        return OrderResponse(**new_order, created_at=None)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create order")

@router.get("/", response_model=OrderListResponse)
async def get_user_orders(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), current_user = Depends(verify_token)):
    """Get user's orders"""
    try:
        _, limit, offset = get_pagination_params(page, limit)
        orders, total = OrderDB.get_user_orders(current_user["user_id"], limit=limit, offset=offset)
        
        return OrderListResponse(
            orders=orders,
            pagination=get_pagination_response(page, limit, total)
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch orders")

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, current_user = Depends(verify_token)):
    """Get order by ID"""
    try:
        order = OrderDB.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        # Check authorization
        if order["user_id"] != current_user["user_id"] and current_user["role"] != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
        
        return OrderResponse(**order)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch order")

@router.get("/admin/all", response_model=OrderListResponse)
async def get_all_orders(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), current_user = Depends(verify_token)):
    """Get all orders (admin only)"""
    try:
        await require_admin(current_user)
        _, limit, offset = get_pagination_params(page, limit)
        orders, total = OrderDB.get_all_orders(limit=limit, offset=offset)
        
        return OrderListResponse(
            orders=orders,
            pagination=get_pagination_response(page, limit, total)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch orders")

@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: int, order: OrderUpdate, current_user = Depends(verify_token)):
    """Update order status (admin only)"""
    try:
        await require_admin(current_user)
        
        existing_order = OrderDB.get_order_by_id(order_id)
        if not existing_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        updated_order = OrderDB.update_order_status(order_id, order.status)
        return OrderResponse(**updated_order)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update order status")

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, current_user = Depends(verify_token)):
    """Delete order (admin only)"""
    try:
        await require_admin(current_user)
        
        existing_order = OrderDB.get_order_by_id(order_id)
        if not existing_order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        OrderDB.delete_order(order_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete order")
