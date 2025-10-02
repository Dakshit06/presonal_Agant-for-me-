"""
Notification service for sending alerts
"""

import structlog

logger = structlog.get_logger()


class NotificationService:
    """Service for sending notifications"""
    
    async def send_approval_request(self, user_id: str, application_id: str, message: str):
        """Send approval request notification"""
        logger.info("Sending approval request", user_id=user_id, application_id=application_id)
    
    async def schedule_reminder(self, user_id: str, application_id: str, days_from_now: int, message: str):
        """Schedule a reminder"""
        logger.info("Scheduling reminder", user_id=user_id, days=days_from_now)
    
    async def send_email(self, user_id: str, subject: str, body: str):
        """Send email notification"""
        logger.info("Sending email", user_id=user_id, subject=subject)
