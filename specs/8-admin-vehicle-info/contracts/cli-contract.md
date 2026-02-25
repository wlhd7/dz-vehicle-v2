# CLI Contract: Admin Vehicle Information

## New Commands

### `vehicle-asset notify-admins`

Scans the asset database for vehicles (KEYs) with:
1. Maintenance dates > 6 months ago.
2. Inspection dates expiring within 30 days.
3. Insurance dates expiring within 30 days.

Sends an aggregated email report to the `ADMIN_NOTIFICATION_EMAIL` using the configured SMTP settings.

**Usage**:
```bash
vehicle-asset notify-admins
```

**Options**:
- `--dry-run`: Scans for warnings and prints the report to stdout without sending an email. Useful for testing and manual checks.
- `--json`: Output the scan results (warnings) in structured JSON format to stdout.

**Output (Success)**:
```
Sent notification email to admin@example.com containing 3 warnings.
```

**Output (No Warnings)**:
```
No vehicle warnings detected. No email sent.
```

**Output (Dry Run)**:
```
[DRY RUN] Would send following warnings to admin@example.com:
- 京A·88888: Maintenance overdue (Last: 2025-01-01)
- 京B·12345: Inspection expires in 15 days (2026-03-12)
```
