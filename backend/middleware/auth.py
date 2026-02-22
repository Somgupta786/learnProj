from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from utils.helpers import verify_token as verify_jwt_token

security = HTTPBearer()

async def verify_token(credentials = Depends(security)) -> dict:
    """Verify JWT token from Authorization header"""
    token = credentials.credentials
    payload = verify_jwt_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return payload

async def require_admin(current_user: dict) -> dict:
    """Check if user is admin"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
