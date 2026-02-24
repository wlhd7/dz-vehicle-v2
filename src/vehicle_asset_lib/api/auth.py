from fastapi import Header, HTTPException, Depends
import uuid
import os
from ..services.auth import validate_admin_secret

# In a real app, we would use JWT or sessions.
# For this prototype, we'll assume the client sends the user_id in a custom header
# after successful verification.

async def get_current_user_id(x_user_id: str = Header(None)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="X-User-ID header missing")
    try:
        uuid.UUID(x_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid User ID format")
    return x_user_id

async def verify_admin_access(x_admin_secret: str = Header(None)):
    """
    Checks if X-Admin-Secret matches the server's ADMIN_SECRET.
    """
    if not validate_admin_secret(x_admin_secret):
        raise HTTPException(
            status_code=403,
            detail="Error: [Access Denied] Missing or invalid ADMIN_SECRET."
        )
    return x_admin_secret
