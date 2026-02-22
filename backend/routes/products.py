from fastapi import APIRouter, HTTPException, Depends, status, Query
from models.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from db.product_db import ProductDB
from utils.helpers import get_pagination_params, get_pagination_response
from middleware.auth import verify_token, require_admin

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=ProductListResponse)
async def get_all_products(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), category: str = None):
    """Get all products with pagination"""
    try:
        _, limit, offset = get_pagination_params(page, limit)
        products, total = ProductDB.get_all_products(limit=limit, offset=offset, category=category)
        
        # Ensure all products have required fields
        processed_products = []
        for product in products:
            if product:
                processed_products.append(product)
        
        return ProductListResponse(
            products=processed_products,
            pagination=get_pagination_response(page, limit, total)
        )
    except Exception as e:
        print(f"ERROR in get_all_products: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch products: {str(e)}")

@router.get("/search", response_model=ProductListResponse)
async def search_products(q: str = Query(...), page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    """Search products"""
    try:
        _, limit, offset = get_pagination_params(page, limit)
        products, total = ProductDB.search_products(q, limit=limit, offset=offset)
        
        return ProductListResponse(
            products=products,
            pagination=get_pagination_response(page, limit, total)
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Search failed")

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """Get product by ID"""
    try:
        product = ProductDB.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return ProductResponse(**product)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch product")

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, current_user = Depends(verify_token)):
    """Create a new product (admin only)"""
    try:
        await require_admin(current_user)
        new_product = ProductDB.create_product(
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            category=product.category,
            image_url=product.image_url
        )
        return ProductResponse(**new_product, created_at=None)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create product")

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductUpdate, current_user = Depends(verify_token)):
    """Update product (admin only)"""
    try:
        await require_admin(current_user)
        existing_product = ProductDB.get_product_by_id(product_id)
        if not existing_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        updated_product = ProductDB.update_product(product_id, **product.dict(exclude_unset=True))
        return ProductResponse(**updated_product)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update product")

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, current_user = Depends(verify_token)):
    """Delete product (admin only)"""
    try:
        await require_admin(current_user)
        existing_product = ProductDB.get_product_by_id(product_id)
        if not existing_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        ProductDB.delete_product(product_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete product")
