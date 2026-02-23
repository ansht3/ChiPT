from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os

REQUIRE_EMAIL_VERIFICATION = os.getenv("REQUIRE_EMAIL_VERIFICATION", "False").lower() == "true"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = "your-secret-key-change-this-in-production"  # Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, role: str, token_version: int = 1) -> str:
    """Create a JWT access token."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "user_id": user_id,
        "role": role,
        "token_version": token_version,
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get current user from JWT token.
    
    Note: This function gets the db session internally to avoid
    circular import issues with FastAPI dependencies.
    """
    from database import User, get_db
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        token_version: int = payload.get("token_version", 1)  # Default to 1 for older tokens
        
        if user_id is None:
            raise credentials_exception
    
    except JWTError:
        raise credentials_exception
    
    # Get database session manually since we can't use Depends(get_db) 
    # in the same function due to circular imports
    async for db in get_db():
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if user is None:
            raise credentials_exception
            
        # Check if the token version matches the database
        if user.token_version != token_version:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been invalidated. Please log in again."
            )
        
        return user
    
    # This should never be reached
    raise credentials_exception


async def require_verified_user(current_user = Depends(get_current_user)):
    """Require that the current user has verified their email."""
    if REQUIRE_EMAIL_VERIFICATION and not current_user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required. Please check your email inbox to verify your account."
        )
    return current_user


def require_global_role(allowed_roles: list[str]):
    """Factory dependency to require specific global roles."""
    async def role_checker(current_user = Depends(require_verified_user)):
        user_role = current_user.global_role if isinstance(current_user.global_role, str) else current_user.global_role.value
        
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Only users with roles {allowed_roles} can access this endpoint"
            )
        return current_user
    return role_checker


# Legacy dependencies for backward compatibility (maps directly to new generalized one)
require_instructor = require_global_role(["instructor", "admin"])


def require_class_instructor(class_id: int):
    """Dependency to require that the current user is an instructor for a specific class."""
    async def role_checker(
        current_user = Depends(require_verified_user),
        # We need the db session to check enrollment, and we do the same pattern as get_current_user
    ):
        from database import get_db, Enrollment, ClassRole
        
        async for db in get_db():
            result = await db.execute(
                select(Enrollment).where(
                    Enrollment.class_id == class_id,
                    Enrollment.user_id == current_user.id
                )
            )
            enrollment = result.scalar_one_or_none()
            
            # Global admins also get access
            user_g_role = current_user.global_role if isinstance(current_user.global_role, str) else current_user.global_role.value
            
            if user_g_role == "admin":
                return current_user
                
            if not enrollment:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not enrolled in this class."
                )
                
            c_role = enrollment.class_role if isinstance(enrollment.class_role, str) else enrollment.class_role.value
            if c_role != "instructor":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You must be an instructor of this class to perform this action."
                )
                
            return current_user
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed"
        )
    return role_checker
