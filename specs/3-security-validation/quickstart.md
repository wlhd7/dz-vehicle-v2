# Quickstart: Enabling Security Access Control

## 1. Configure Secret
Create or update your `.env` file in the project root:

```bash
ADMIN_SECRET=your_secure_random_string
```

## 2. Using the CLI
Always prefix admin commands with the secret if not exported:

```bash
ADMIN_SECRET=your_secure_random_string vehicle-asset admin list-users
```

## 3. Using the API
Include the header in your HTTP requests:

```bash
curl -H "X-Admin-Secret: your_secure_random_string" http://localhost:8000/admin/users
```
