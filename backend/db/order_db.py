import psycopg2
import psycopg2.extras
from typing import Optional, Tuple
from config.database import get_db_connection, close_db_connection

class OrderDB:
    @staticmethod
    def create_order(user_id: int, total_amount: float, shipping_address: str, status: str = "pending") -> dict:
        """Create a new order"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = "INSERT INTO orders (user_id, total_amount, status, shipping_address, created_at) VALUES (%s, %s, %s, %s, NOW()) RETURNING id"
            cursor.execute(query, (user_id, total_amount, status, shipping_address))
            conn.commit()
            order_id = cursor.fetchone()[0]
            return {"id": order_id, "user_id": user_id, "total_amount": total_amount, "status": status}
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def get_order_by_id(order_id: int) -> Optional[dict]:
        """Get order by ID"""
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            query = "SELECT * FROM orders WHERE id = %s"
            cursor.execute(query, (order_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def get_user_orders(user_id: int, limit: int = 10, offset: int = 0) -> Tuple[list, int]:
        """Get orders by user ID"""
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            query = "SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC LIMIT %s OFFSET %s"
            cursor.execute(query, (user_id, limit, offset))
            orders = cursor.fetchall()

            count_query = "SELECT COUNT(*) as total FROM orders WHERE user_id = %s"
            cursor.execute(count_query, (user_id,))
            total = cursor.fetchone()["total"]

            return orders, total
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def get_all_orders(limit: int = 10, offset: int = 0) -> Tuple[list, int]:
        """Get all orders (admin)"""
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            query = "SELECT * FROM orders ORDER BY created_at DESC LIMIT %s OFFSET %s"
            cursor.execute(query, (limit, offset))
            orders = cursor.fetchall()

            count_query = "SELECT COUNT(*) as total FROM orders"
            cursor.execute(count_query)
            total = cursor.fetchone()["total"]

            return orders, total
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def update_order_status(order_id: int, status: str) -> Optional[dict]:
        """Update order status"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

            query = "UPDATE orders SET status = %s WHERE id = %s"
            cursor.execute(query, (status, order_id))
            conn.commit()

            return OrderDB.get_order_by_id(order_id)
        finally:
            cursor.close()
            close_db_connection(conn)

    @staticmethod
    def delete_order(order_id: int) -> bool:
        """Delete order"""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = "DELETE FROM orders WHERE id = %s"
            cursor.execute(query, (order_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            close_db_connection(conn)
