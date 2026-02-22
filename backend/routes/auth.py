from fastapi import APIRouter, HTTPException, status
from models.user import UserCreate, UserLogin, UserResponse, TokenResponse
from db.user_db import UserDB
from utils.helpers import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """Register a new user"""
    try:
        new_user = UserDB.create_user(
            name=user.name,
            email=user.email,
            password=user.password,
            phone=user.phone
        )
        return UserResponse(**new_user, created_at=None)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login user"""
    try:
        user = UserDB.get_user_by_email(credentials.email)
        if not user or not UserDB.verify_password(credentials.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token = create_access_token(user["id"], user["role"])
        return TokenResponse(
            access_token=token,
            user=UserResponse(**user)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed")
