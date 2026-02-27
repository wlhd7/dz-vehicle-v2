# API Contract: Admin OTP Management Panel

## Endpoints

### 1. Get OTP Count
**GET /admin/otp/count**

**Response (200 OK):**
```json
{
  "count": 145
}
```

---

### 2. Add Single OTP
**POST /admin/otp/single**

**Request:**
```json
{
  "password": "12345678"
}
```

**Response (200 OK):**
```json
{
  "message": "OTP added successfully",
  "total_pool": 146
}
```

---

### 3. Batch Upload OTPs
**POST /admin/otp/batch**

**Request (multipart/form-data):**
- `file`: .txt or .csv file containing OTPs.

**Response (200 OK):**
```json
{
  "added": 100,
  "skipped": 5,
  "total_pool": 241
}
```

**Response (400 Bad Request) - Atomic Failure:**
```json
{
  "detail": "文件中包含无效的 OTP 格式"
}
```

## Security
- Requires `ADMIN_SECRET` in header (`X-Admin-Secret`).
- Access restricted by the designated `user_id` on the frontend side.
