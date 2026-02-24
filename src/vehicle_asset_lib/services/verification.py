from sqlalchemy.orm import Session
from ..models import User, UserStatus

class VerificationService:
    def __init__(self, db: Session):
        self.db = db

    def verify_user(self, name: str, id_last4: str) -> dict:
        user = self.db.query(User).filter(User.name == name, User.id_last4 == id_last4).first()
        
        if not user:
            return {"success": False, "message": "Invalid name or ID digits"}
        
        if user.status != UserStatus.ACTIVE:
            return {"success": False, "message": "User account is inactive"}
        
        return {
            "success": True, 
            "user_id": str(user.id), 
            "message": "Authenticated"
        }
