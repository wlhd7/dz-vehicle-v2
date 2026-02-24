# API Contract: Security Requirements

## Administrative Endpoints
All endpoints under `/admin/*` require authentication.

### Authentication Header
- **Key**: `X-Admin-Secret`
- **Value**: The value must match the `ADMIN_SECRET` configured on the server.

### Responses
- **403 Forbidden**: Returned if the header is missing, incorrect, or empty.
  - Body: `{"detail": "Access Denied: Invalid Admin Secret"}`
- **200 OK / 201 Created**: Returned if authentication succeeds (proceeds to normal operation).

### Example Request
```http
POST /admin/assets
X-Admin-Secret: topsecret
Content-Type: application/json

{
  "type": "KEY",
  "identifier": "PLATE-123"
}
```
