import logging
import uuid
from typing import Optional

logger = logging.getLogger(__name__)

def generate_verification_token() -> str:
    """Generate a secure, random verification token."""
    return str(uuid.uuid4())

async def send_verification_email(email: str, token: str) -> bool:
    """
    Stub for sending a verification email.
    In a real system, this would use SMTP, SendGrid, AWS SES, etc.
    """
    logger.info(f"========== EMAIL VERIFICATION STUB ==========")
    logger.info(f"To: {email}")
    logger.info(f"Subject: Please verify your ChiPT account")
    logger.info(f"Body: Use the following token to verify your account or click the link:")
    logger.info(f"      Token: {token}")
    logger.info(f"      Link:  http://localhost:8000/api/verify-email?token={token}&email={email}") # Example frontend link
    logger.info(f"=============================================")
    
    # Simulate email sending delay
    # await asyncio.sleep(0.5)
    
    return True
