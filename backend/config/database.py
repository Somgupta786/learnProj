import psycopg2
from psycopg2 import Error, pool
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

# Connection pool configuration
_connection_pool = None

def initialize_connection_pool():
    """Initialize connection pool"""
    global _connection_pool
    try:
        _connection_pool = pool.SimpleConnectionPool(
            1,
            20,
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        print("✓ Connection pool initialized successfully")
    except Error as e:
        print(f"✗ Failed to initialize connection pool: {e}")
        raise e

def get_db_connection():
    """Get a database connection from the pool"""
    global _connection_pool
    if _connection_pool is None:
        initialize_connection_pool()
    try:
        connection = _connection_pool.getconn()
        return connection
    except Error as e:
        print(f"✗ Database connection failed: {e}")
        raise e

def close_db_connection(connection):
    """Return connection to the pool"""
    global _connection_pool
    if connection and _connection_pool:
        _connection_pool.putconn(connection)
