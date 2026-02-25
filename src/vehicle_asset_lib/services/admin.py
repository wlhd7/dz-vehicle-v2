from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from ..models import User, Asset, OTPPool, AssetType, UserStatus, AssetStatus

class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def add_asset(self, type: AssetType, identifier: str, maintenance_date=None, maintenance_mileage=None, inspection_date=None, insurance_date=None) -> Asset:
        asset = Asset(
            type=type, 
            identifier=identifier,
            maintenance_date=maintenance_date,
            maintenance_mileage=maintenance_mileage,
            inspection_date=inspection_date,
            insurance_date=insurance_date
        )
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def get_asset(self, asset_id: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.id == uuid.UUID(asset_id)).first()

    def update_asset(self, asset_id: str, identifier: Optional[str] = None, type: Optional[AssetType] = None, status: Optional[AssetStatus] = None, maintenance_date=None, maintenance_mileage=None, inspection_date=None, insurance_date=None) -> Optional[Asset]:
        asset = self.get_asset(asset_id)
        if not asset:
            return None
        
        if identifier is not None:
            asset.identifier = identifier
        if type is not None:
            asset.type = type
        if status is not None:
            asset.status = status
        if maintenance_date is not None:
            asset.maintenance_date = maintenance_date
        if maintenance_mileage is not None:
            asset.maintenance_mileage = maintenance_mileage
        if inspection_date is not None:
            asset.inspection_date = inspection_date
        if insurance_date is not None:
            asset.insurance_date = insurance_date
            
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def delete_asset(self, asset_id: str) -> bool:
        asset = self.get_asset(asset_id)
        if not asset:
            return False
        
        self.db.delete(asset)
        self.db.commit()
        return True

    def list_users(self) -> List[User]:
        return self.db.query(User).all()

    def add_user(self, name: str, id_last4: str) -> User:
        user = User(name=name, id_last4=id_last4)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == uuid.UUID(user_id)).first()

    def update_user(self, user_id: str, name: Optional[str] = None, id_last4: Optional[str] = None, status: Optional[UserStatus] = None) -> Optional[User]:
        user = self.get_user(user_id)
        if not user:
            return None
        
        if name is not None:
            user.name = name
        if id_last4 is not None:
            user.id_last4 = id_last4
        if status is not None:
            user.status = status
            
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: str) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        return True

    def batch_add_users(self, pairs: List[tuple]) -> dict:
        added = 0
        skipped = 0
        for name, id_last4 in pairs:
            exists = self.db.query(User).filter(User.name == name, User.id_last4 == id_last4).first()
            if exists:
                skipped += 1
                continue
            
            user = User(name=name, id_last4=id_last4)
            self.db.add(user)
            added += 1
        
        self.db.commit()
        return {"added": added, "skipped": skipped, "total": len(pairs)}

    def seed_otps(self, passwords: List[str]) -> dict:
        added = 0
        skipped = 0
        for pwd in passwords:
            # Check for unused OTP with the same password
            exists = self.db.query(OTPPool).filter(OTPPool.password == pwd, OTPPool.is_used == False).first()
            if exists:
                skipped += 1
                continue
                
            otp = OTPPool(password=pwd)
            self.db.add(otp)
            added += 1
        self.db.commit()
        
        total = self.db.query(OTPPool).count()
        return {"added": added, "skipped": skipped, "total_pool": total}
