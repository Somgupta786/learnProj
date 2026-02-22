import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "ecommerce_db")
DB_PORT = int(os.getenv("DB_PORT", 5432))

# Server Configuration
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
NODE_ENV = os.getenv("NODE_ENV", "development")

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your_super_secret_jwt_key_change_this_in_production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_DAYS = 7

# CORS Configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")

# Database URL for SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
