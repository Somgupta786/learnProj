from datetime import datetime, timedelta
import jwt
from typing import Optional, Dict
from config.settings import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_DAYS

def create_access_token(user_id: int, role: str) -> str:
    """Create JWT access token"""
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(days=JWT_EXPIRE_DAYS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def verify_token(token: str) -> Optional[Dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_pagination_params(page: int = 1, limit: int = 10) -> tuple:
    """Calculate pagination offset"""
    page = max(1, page)
    limit = max(1, min(100, limit))
    offset = (page - 1) * limit
    return page, limit, offset

def get_pagination_response(current_page: int, limit: int, total: int) -> Dict:
    """Generate pagination metadata"""
    total_pages = (total + limit - 1) // limit
    return {
        "current_page": current_page,
        "total_pages": total_pages,
        "total_items": total,
        "items_per_page": limit
    }
