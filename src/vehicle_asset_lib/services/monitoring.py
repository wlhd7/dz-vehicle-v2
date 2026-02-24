import logging
from sqlalchemy.orm import Session
from ..models import OTPPool

class MonitoringService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def check_otp_threshold(self, threshold: int = 30) -> dict:
        available_count = self.db.query(OTPPool).filter(OTPPool.is_used == False).count()
        
        if available_count < threshold:
            message = f"Low OTP threshold alert: only {available_count} codes remaining (threshold: {threshold})"
            self.logger.warning(message)
            # Placeholder for email notification
            self._send_email_placeholder(message)
            return {"triggered": True, "message": message, "count": available_count}
            
        return {"triggered": False, "count": available_count}

    def _send_email_placeholder(self, message: str):
        # Implementation of actual email sending would go here.
        pass
