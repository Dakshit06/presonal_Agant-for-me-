"""
API dependencies
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current authenticated user"""
    # Placeholder - implement JWT verification
    from src.models.database import User
    return User(id="user-123", email="user@example.com", name="Test User")
