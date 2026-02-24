# CLI Contract: Security Requirements

## Invocation Pattern
Administrative commands must be preceded by the `ADMIN_SECRET` environment variable or have it set in the environment.

### Authorized Example
```bash
ADMIN_SECRET=topsecret vehicle-asset admin list-users
```

### Unauthorized Example
```bash
vehicle-asset admin list-users
# Expected Output: Error: [Access Denied] Missing or invalid ADMIN_SECRET.
# Expected Exit Code: 1
```

## Environment Variables
- `ADMIN_SECRET`: Required for all `admin` subcommands.
