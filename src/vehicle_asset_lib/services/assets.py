import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import User, Asset, OTPPool, AssetStatus, AssetType, TransactionLog, TransactionAction

class AssetService:
    def __init__(self, db: Session):
        self.db = db

    def list_assets(self, asset_type: str = "all") -> List[dict]:
        query = self.db.query(Asset)
        if asset_type != "all":
            query = query.filter(Asset.type == asset_type.upper())
        
        assets = query.all()
        result = []
        for a in assets:
            item = {
                "id": str(a.id),
                "type": a.type.value,
                "identifier": a.identifier,
                "status": a.status.value,
                "current_holder_id": str(a.current_holder_id) if a.current_holder_id else None
            }
            if a.type.value == "KEY":
                def safe_iso(dt):
                    if dt and hasattr(dt, 'isoformat'):
                        return dt.isoformat() + "Z"
                    return dt # Return as is if already a string or None
                
                item["maintenance_date"] = safe_iso(a.maintenance_date)
                item["maintenance_mileage"] = a.maintenance_mileage
                item["inspection_date"] = safe_iso(a.inspection_date)
                item["insurance_date"] = safe_iso(a.insurance_date)
            result.append(item)
        return result

    def list_active_loans(self) -> List[dict]:
        from sqlalchemy import func
        
        # Subquery to find the latest PICKUP timestamp for each asset
        latest_pickup = self.db.query(
            TransactionLog.asset_id,
            func.max(TransactionLog.timestamp).label("latest_ts")
        ).filter(TransactionLog.action == TransactionAction.PICKUP).group_by(TransactionLog.asset_id).subquery()

        query = self.db.query(Asset, User.name, latest_pickup.c.latest_ts)\
            .join(User, Asset.current_holder_id == User.id)\
            .join(latest_pickup, Asset.id == latest_pickup.c.asset_id)\
            .filter(Asset.status == AssetStatus.CHECKED_OUT)\
            .order_by(latest_pickup.c.latest_ts.desc())

        results = query.all()
        return [
            {
                "identifier": asset.identifier,
                "type": asset.type.value,
                "user": username,
                "timestamp": timestamp.isoformat() + "Z"
            } for asset, username, timestamp in results
        ]

    def list_loan_records(self, limit: int = 200) -> List[dict]:
        from sqlalchemy import func, select
        
        # Correlated subquery for return_time
        t2 = TransactionLog.__table__.alias("t2")
        return_time_subquery = (
            select(func.min(t2.c.timestamp))
            .where(
                t2.c.asset_id == TransactionLog.asset_id,
                t2.c.action == TransactionAction.RETURN,
                t2.c.timestamp > TransactionLog.timestamp
            )
            .correlate(TransactionLog)
            .as_scalar()
        )

        query = self.db.query(
            Asset.identifier,
            Asset.type,
            User.name.label("user_name"),
            TransactionLog.timestamp.label("loan_time"),
            return_time_subquery.label("return_time")
        ).join(Asset, TransactionLog.asset_id == Asset.id)\
         .join(User, TransactionLog.user_id == User.id)\
         .filter(TransactionLog.action == TransactionAction.PICKUP)\
         .order_by(TransactionLog.timestamp.desc())\
         .limit(limit)

        results = query.all()
        
        def safe_iso(dt):
            if dt and hasattr(dt, 'isoformat'):
                return dt.isoformat() + "Z"
            return None

        return [
            {
                "identifier": r.identifier,
                "type": r.type.value,
                "user_name": r.user_name,
                "loan_time": safe_iso(r.loan_time),
                "return_time": safe_iso(r.return_time)
            } for r in results
        ]

    def list_all_identifiers(self) -> List[str]:
        from sqlalchemy import union
        
        # Get identifiers from assets table
        asset_ids = self.db.query(Asset.identifier)
        
        # Also get identifiers from transaction logs to include deleted assets with history
        log_ids = self.db.query(Asset.identifier).join(TransactionLog, Asset.id == TransactionLog.asset_id)
        
        # Union and distinct
        all_ids = asset_ids.union(log_ids).distinct().all()
        return [r[0] for r in all_ids]

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
            "expires_at": (datetime.utcnow() + timedelta(hours=2)).isoformat() + "Z"
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
            "message": f"Return code generated for {len(assets)} assets",
            "expires_at": (datetime.utcnow() + timedelta(hours=2)).isoformat() + "Z"
        }
