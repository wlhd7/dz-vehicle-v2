import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import User, Asset, OTPPool, AssetStatus, TransactionLog, TransactionAction

class AssetService:
    def __init__(self, db: Session):
        self.db = db

    def list_assets(self, type: str = "all") -> List[dict]:
        query = self.db.query(Asset)
        if type != "all":
            query = query.filter(Asset.type == type.upper())
        
        assets = query.all()
        return [
            {
                "id": str(a.id),
                "type": a.type.value,
                "identifier": a.identifier,
                "status": a.status.value
            } for a in assets
        ]

    def pickup(self, user_id: str, asset_ids: List[str]) -> dict:
        user = self.db.query(User).filter(User.id == uuid.UUID(user_id)).first()
        if not user:
            return {"success": False, "message": "User not found"}
        
        assets = self.db.query(Asset).filter(Asset.id.in_([uuid.UUID(aid) for aid in asset_ids])).with_for_update().all()
        
        if len(assets) != len(asset_ids):
            return {"success": False, "message": "One or more assets not found"}
        
        for asset in assets:
            if asset.status != AssetStatus.AVAILABLE:
                return {"success": False, "message": f"Asset {asset.identifier} is already checked out"}
        
        otp = self.db.query(OTPPool).filter(OTPPool.is_used == False).with_for_update().first()
        if not otp:
            # Block & Notify: System should ideally log/notify admin here.
            # T022 will handle low threshold alerts.
            return {"success": False, "message": "No codes available. Please contact admin."}
        
        # Update states
        otp.is_used = True
        otp.used_at = datetime.utcnow()
        
        asset_identifiers = []
        for asset in assets:
            asset.status = AssetStatus.CHECKED_OUT
            asset.current_holder_id = user.id
            asset_identifiers.append(asset.identifier)
            
            # Log transaction
            log = TransactionLog(
                user_id=user.id,
                asset_id=asset.id,
                action=TransactionAction.PICKUP,
                otp_id=otp.id
            )
            self.db.add(log)
            
        self.db.commit()
        
        return {
            "success": True,
            "otp": otp.password,
            "assets": asset_identifiers,
            "expires_at": str(datetime.utcnow()) # Placeholder for expiry logic
        }

    def return_asset(self, user_id: str, asset_id: str) -> dict:
        user = self.db.query(User).filter(User.id == uuid.UUID(user_id)).first()
        if not user:
            return {"success": False, "message": "User not found"}
        
        asset = self.db.query(Asset).filter(Asset.id == uuid.UUID(asset_id)).with_for_update().first()
        if not asset:
            return {"success": False, "message": "Asset not found"}
        
        if asset.status != AssetStatus.CHECKED_OUT:
            return {"success": False, "message": "Asset is not checked out"}
            
        if asset.current_holder_id != user.id:
            return {"success": False, "message": "You are not the holder of this asset"}
            
        otp = self.db.query(OTPPool).filter(OTPPool.is_used == False).with_for_update().first()
        if not otp:
            return {"success": False, "message": "No codes available. Please contact admin."}
            
        # Update states
        otp.is_used = True
        otp.used_at = datetime.utcnow()
        
        asset.status = AssetStatus.AVAILABLE
        asset.current_holder_id = None
        
        # Log transaction
        log = TransactionLog(
            user_id=user.id,
            asset_id=asset.id,
            action=TransactionAction.RETURN,
            otp_id=otp.id
        )
        self.db.add(log)
        
        self.db.commit()
        
        return {
            "success": True,
            "otp": otp.password,
            "message": "Return code generated"
        }
