import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import List

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.server = os.getenv("SMTP_SERVER", "localhost")
        self.port = int(os.getenv("SMTP_PORT", "587"))
        self.user = os.getenv("SMTP_USER", "")
        self.password = os.getenv("SMTP_PASSWORD", "")
        self.use_tls = os.getenv("SMTP_TLS", "True").lower() in ("true", "1", "yes")
        self.admin_email = os.getenv("ADMIN_NOTIFICATION_EMAIL", "")

    def _build_email_body(self, alerts: List[dict]) -> str:
        body = "<h3>Vehicle Alerts</h3><ul>"
        for alert in alerts:
            body += f"<li><b>{alert['identifier']}</b>: {alert['alert_type']} - {alert['status']} (Date: {alert['date']})</li>"
        body += "</ul>"
        return body

    def send_admin_alert(self, alerts: List[dict]) -> bool:
        if not self.admin_email:
            logger.error("ADMIN_NOTIFICATION_EMAIL not set, cannot send email.")
            return False

        if not alerts:
            return True

        msg = MIMEMultipart()
        msg['From'] = self.user or "noreply@dz-vehicle"
        msg['To'] = self.admin_email
        msg['Subject'] = f"DZ Vehicle Notification: {len(alerts)} Warnings"
        
        body = self._build_email_body(alerts)
        msg.attach(MIMEText(body, 'html'))

        try:
            # We use SMTP for general connect, though it might fail if we don't have a real server
            # So we catch connection errors and log them
            server = smtplib.SMTP(self.server, self.port)
            if self.use_tls:
                server.starttls()
            if self.user and self.password:
                server.login(self.user, self.password)
            server.send_message(msg)
            server.quit()
            logger.info(f"Email sent successfully to {self.admin_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
