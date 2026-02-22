from typing import Optional, Tuple
from config.database import get_db_connection, close_db_connection
from utils.validators import validate_price, validate_stock

class ProductDB:
    @staticmethod
    def create_product(name: str, description: str = None, price: float = None, 
                      stock: int = None, category: str = None, image_url: str = None) -> dict:
        """Create a new product"""
        if not validate_price(price):
            raise ValueError("Price must be a positive number")
        
        if not validate_stock(stock):
            raise ValueError("Stock must be a non-negative integer")

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = "INSERT INTO products (name, description, price, stock, category, image_url, created_at) VALUES (%s, %s, %s, %s, %s, %s, NOW()) RETURNING id, name, price, stock"
            cursor.execute(query, (name, description, price, stock, category, image_url))
            conn.commit()
            result = cursor.fetchone()
            return {"id": result[0], "name": result[1], "price": result[2], "stock": result[3]}
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[dict]:
        """Get product by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = "SELECT id, name, description, price, stock, category, image_url, created_at FROM products WHERE id = %s"
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            if result:
                return {
                    "id": result[0],
                    "name": result[1],
                    "description": result[2],
                    "price": result[3],
                    "stock": result[4],
                    "category": result[5],
                    "image_url": result[6],
                    "created_at": result[7]
                }
            return None
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def get_all_products(limit: int = 10, offset: int = 0, category: str = None) -> Tuple[list, int]:
        """Get all products with pagination"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            if category:
                query = "SELECT id, name, description, price, stock, category, image_url, created_at FROM products WHERE category = %s LIMIT %s OFFSET %s"
                cursor.execute(query, (category, limit, offset))
            else:
                query = "SELECT id, name, description, price, stock, category, image_url, created_at FROM products LIMIT %s OFFSET %s"
                cursor.execute(query, (limit, offset))

            results = cursor.fetchall()
            products = []
            for row in results:
                products.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "price": row[3],
                    "stock": row[4],
                    "category": row[5],
                    "image_url": row[6],
                    "created_at": row[7]
                })

            if category:
                count_query = "SELECT COUNT(*) FROM products WHERE category = %s"
                cursor.execute(count_query, (category,))
            else:
                count_query = "SELECT COUNT(*) FROM products"
                cursor.execute(count_query)

            total = cursor.fetchone()[0]
            return products, total
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def update_product(product_id: int, **kwargs) -> Optional[dict]:
        """Update product"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            allowed_fields = ["name", "description", "price", "stock", "category", "image_url"]
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}

            if not updates:
                return ProductDB.get_product_by_id(product_id)

            set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
            values = list(updates.values()) + [product_id]

            query = f"UPDATE products SET {set_clause} WHERE id = %s"
            cursor.execute(query, values)
            conn.commit()

            return ProductDB.get_product_by_id(product_id)
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def delete_product(product_id: int) -> bool:
        """Delete product"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = "DELETE FROM products WHERE id = %s"
            cursor.execute(query, (product_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def search_products(search_term: str, limit: int = 10, offset: int = 0) -> Tuple[list, int]:
        """Search products"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            search_term = f"%{search_term}%"
            query = "SELECT id, name, description, price, stock, category, image_url, created_at FROM products WHERE name ILIKE %s OR description ILIKE %s LIMIT %s OFFSET %s"
            cursor.execute(query, (search_term, search_term, limit, offset))
            results = cursor.fetchall()
            
            products = []
            for row in results:
                products.append({
                    "id": row[0],
                    "name": row[1],
                    "description": row[2],
                    "price": row[3],
                    "stock": row[4],
                    "category": row[5],
                    "image_url": row[6],
                    "created_at": row[7]
                })

            count_query = "SELECT COUNT(*) FROM products WHERE name ILIKE %s OR description ILIKE %s"
            cursor.execute(count_query, (search_term, search_term))
            total = cursor.fetchone()[0]

            return products, total
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def decrease_stock(product_id: int, quantity: int) -> bool:
        """Decrease product stock"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = "UPDATE products SET stock = stock - %s WHERE id = %s AND stock >= %s"
            cursor.execute(query, (quantity, product_id, quantity))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            close_db_connection(conn)
