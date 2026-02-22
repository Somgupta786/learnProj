import psycopg2
from psycopg2 import Error
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

# Connection pool configuration
def get_db_connection():
    """Create a database connection"""
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return connection
    except Error as e:
        print(f"✗ Database connection failed: {e}")
        raise e

def close_db_connection(connection):
    """Close database connection"""
    if connection:
        connection.close()

