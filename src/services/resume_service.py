"""
Resume service for managing resumes
"""

from typing import Optional
from src.models.database import Resume
from src.database.session import get_db


class ResumeService:
    """Service for managing resumes"""
    
    async def get_current_resume(self, user_id: str) -> Optional[Resume]:
        """Get user's current resume"""
        
        async with get_db() as db:
            resume = await db.query(Resume).filter(
                Resume.user_id == user_id,
                Resume.is_current == True
            ).first()
            return resume
