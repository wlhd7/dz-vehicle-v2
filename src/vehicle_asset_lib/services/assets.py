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

        # Check limits (max 1 of each type)
        held_assets = self.db.query(Asset).filter(Asset.current_holder_id == user.id, Asset.status == AssetStatus.CHECKED_OUT).all()
        held_types = {a.type for a in held_assets}
        
        requested_types = [a.type for a in assets]
        from collections import Counter
        requested_counts = Counter(requested_types)
        
        for t, count in requested_counts.items():
            type_label = "vehicle" if t.value == "KEY" else t.value.lower().replace('_', ' ')
            if count > 1:
                return {"success": False, "message": f"You cannot borrow more than one {type_label}"}
            if t in held_types:
                return {"success": False, "message": f"You already hold a {type_label}"}
        
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
        return self.return_assets(user_id, [asset_id])

    def return_assets(self, user_id: str, asset_ids: List[str]) -> dict:
        user = self.db.query(User).filter(User.id == uuid.UUID(user_id)).first()
        if not user:
            return {"success": False, "message": "User not found"}
        
        assets = self.db.query(Asset).filter(Asset.id.in_([uuid.UUID(aid) for aid in asset_ids])).with_for_update().all()
        if not assets:
            return {"success": False, "message": "No assets found to return"}

        for asset in assets:
            if asset.status != AssetStatus.CHECKED_OUT:
                return {"success": False, "message": f"Asset {asset.identifier} is not checked out"}
            if asset.current_holder_id != user.id:
                return {"success": False, "message": f"You are not the holder of asset {asset.identifier}"}
            
        otp = self.db.query(OTPPool).filter(OTPPool.is_used == False).with_for_update().first()
        if not otp:
            return {"success": False, "message": "No codes available. Please contact admin."}
            
        # Update states
        otp.is_used = True
        otp.used_at = datetime.utcnow()
        
        for asset in assets:
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
            "message": f"Return code generated for {len(assets)} assets"
        }
