import os
from typing import Optional

def get_admin_secret() -> Optional[str]:
    """
    Retrieve the ADMIN_SECRET from environment variables.
    """
    return os.getenv("ADMIN_SECRET")

def validate_admin_secret(provided_secret: Optional[str]) -> bool:
    """
    Validate the provided secret against the configured ADMIN_SECRET.
    Returns True if valid, False otherwise.
    Default secure: if ADMIN_SECRET is not set, all validation fails.
    """
    configured_secret = get_admin_secret()
    if not configured_secret:
        return False
    return provided_secret == configured_secret
