# Quickstart: Admin Vehicle Information

## Environment Setup
Add the following to your local `.env` file to configure email notifications:

```env
ADMIN_NOTIFICATION_EMAIL=admin@yourcompany.com
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USER=your_smtp_username
SMTP_PASSWORD=your_smtp_password
SMTP_TLS=True
```

## Running the Web Interface
1. Start the API server:
   ```bash
   uvicorn src.vehicle_asset_lib.api.main:app --reload
   ```
2. Start the Frontend dev server:
   ```bash
   cd frontend
   npm run dev
   ```

## Testing Notifications Manually
You can manually trigger the notification check using the Typer CLI:

1. Test without sending an email (dry run):
   ```bash
   vehicle-asset notify-admins --dry-run
   ```

2. Test sending a real email:
   ```bash
   vehicle-asset notify-admins
   ```

## Production Scheduling
On a production server, set up a cron job to run the notification check weekly (e.g., every Monday at 9:00 AM):

```cron
0 9 * * 1 cd /path/to/project && /path/to/venv/bin/vehicle-asset notify-admins >> /var/log/vehicle-notifications.log 2>&1
```
