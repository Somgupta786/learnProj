import os
from dotenv import load_dotenv

load_dotenv()

# Environment
NODE_ENV = os.getenv("NODE_ENV", "development")

# Database Configuration
# In production, these MUST be set via environment variables
if NODE_ENV == "production":
    # Production: Require all values to be explicitly set
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
        raise ValueError("Missing required database environment variables in production")
else:
    # Development: Allow localhost defaults
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "ecommerce_db")

DB_PORT = int(os.getenv("DB_PORT", 5432))

# Server Configuration
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    if NODE_ENV == "production":
        raise ValueError("JWT_SECRET must be set for production")
    else:
        JWT_SECRET = "dev_secret_key_change_in_production_12345"

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_DAYS = 7

# CORS Configuration
FRONTEND_URL = os.getenv("FRONTEND_URL")
if not FRONTEND_URL:
    if NODE_ENV == "production":
        raise ValueError("FRONTEND_URL must be set for production")
    else:
        FRONTEND_URL = "http://localhost:8501"

# Database URL for SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
