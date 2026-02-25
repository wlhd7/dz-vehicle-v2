# Data Model: Admin Vehicle Information

## Entities

### `Asset` (Updated)
We need to track four additional, optional fields on the `Asset` model to support vehicle maintenance and compliance features. Since `AssetType.GAS_CARD` does not use these, they must be nullable.

#### Added Fields
- `maintenance_date` (`DateTime`, Optional): Records the date of the last maintenance service.
- `maintenance_mileage` (`Integer`, Optional): Records the mileage at the last maintenance service.
- `inspection_date` (`DateTime`, Optional): Records the expiration date of the vehicle's annual inspection.
- `insurance_date` (`DateTime`, Optional): Records the expiration date of the vehicle's insurance policy.

#### Existing Fields (for Context)
- `id`: UUID (Primary Key)
- `type`: AssetType (KEY / GAS_CARD)
- `identifier`: String (e.g., license plate)
- `status`: AssetStatus
- `current_holder_id`: Optional[UUID]

## Validation Rules
- The newly added fields (`maintenance_date`, `maintenance_mileage`, `inspection_date`, `insurance_date`) apply semantically only to `AssetType.KEY`.
- Validation should ensure they are stored or updated correctly, allowing nulls when the asset is not a vehicle or the data hasn't been set.

## Environment Configuration
The following `.env` variables will be introduced to handle email notifications:
- `ADMIN_NOTIFICATION_EMAIL` (String): The recipient email address for alerts.
- `SMTP_SERVER` (String): SMTP server host (e.g., `smtp.example.com`).
- `SMTP_PORT` (Integer): SMTP server port (e.g., 587 or 465).
- `SMTP_USER` (String): SMTP username.
- `SMTP_PASSWORD` (String): SMTP password.
- `SMTP_TLS` (Boolean): Whether to use STARTTLS (default `True`).
