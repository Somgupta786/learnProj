from fastapi import APIRouter, HTTPException, status
from models.user import UserCreate, UserLogin, UserResponse, TokenResponse
from db.user_db import UserDB
from utils.helpers import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """Register a new user"""
    try:
        new_user = UserDB.create_user(
            name=user.name,
            email=user.email,
            password=user.password,
            phone=user.phone
        )
        return {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "phone": new_user.get("phone"),
            "role": new_user["role"],
            "created_at": str(new_user.get("created_at")) if new_user.get("created_at") else None
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")

@router.post("/login")
async def login(credentials: UserLogin):
    """Login user"""
    try:
        print(f"[LOGIN] Attempting login for: {credentials.email}")
        user = UserDB.get_user_by_email(credentials.email)
        print(f"[LOGIN] User found: {user is not None}")
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        password_valid = UserDB.verify_password(credentials.password, user["password"])
        print(f"[LOGIN] Password valid: {password_valid}")
        
        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token = create_access_token(user["id"], user["role"])
        print(f"[LOGIN] Token created. User role: {user['role']}")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "phone": user.get("phone"),
                "role": user["role"],
                "created_at": str(user.get("created_at")) if user.get("created_at") else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[LOGIN_ERROR] Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Login failed: {str(e)}")



