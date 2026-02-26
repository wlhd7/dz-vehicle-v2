# Monitoring & Alerts

## Vehicle Maintenance
- **Threshold**: Maintenance is overdue if `last_maintenance_date` > 6 months ago.
- **Alert Level**: Warning (Orange UI Highlight).

## Compliance Tracking
- **Threshold**: Annual Inspection or Insurance is expiring within 30 days.
- **Alert Level**: Critical/Warning.

## OTP Threshold
- **Threshold**: Warning triggered when available (unused) OTPs in `OTPPool` drop below 30.

## Notifications
- **Email**: Weekly summary sent to `ADMIN_NOTIFICATION_EMAIL`.
- **CLI**: `vehicle-asset notify-admins --dry-run` to inspect current alerts.
