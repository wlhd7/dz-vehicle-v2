import logging
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from ..models import OTPPool, Asset, AssetType

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

    def check_vehicle_alerts(self) -> List[dict]:
        now = datetime.utcnow()
        vehicles = self.db.query(Asset).filter(Asset.type == AssetType.KEY).all()
        alerts = []
        
        for v in vehicles:
            if v.maintenance_date:
                diff_months = (now.year - v.maintenance_date.year) * 12 + now.month - v.maintenance_date.month
                if diff_months >= 6:
                    alerts.append({
                        "identifier": v.identifier,
                        "alert_type": "Maintenance",
                        "date": v.maintenance_date.strftime("%Y-%m-%d"),
                        "status": "Maintenance overdue (>6 months)"
                    })
            if v.inspection_date:
                diff_days = (v.inspection_date - now).days
                if 0 <= diff_days <= 30:
                    alerts.append({
                        "identifier": v.identifier,
                        "alert_type": "Inspection",
                        "date": v.inspection_date.strftime("%Y-%m-%d"),
                        "status": f"Inspection expiring in {diff_days} days"
                    })
            if v.insurance_date:
                diff_days = (v.insurance_date - now).days
                if 0 <= diff_days <= 30:
                    alerts.append({
                        "identifier": v.identifier,
                        "alert_type": "Insurance",
                        "date": v.insurance_date.strftime("%Y-%m-%d"),
                        "status": f"Insurance expiring in {diff_days} days"
                    })
        return alerts

    def _send_email_placeholder(self, message: str):
        # Implementation of actual email sending would go here.
        pass
