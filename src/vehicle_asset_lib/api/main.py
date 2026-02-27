from typing import List, Optional
import uuid
from fastapi import FastAPI, Depends, HTTPException, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dotenv import load_dotenv
from ..db import SessionLocal, init_db
from ..services.verification import VerificationService
from ..services.assets import AssetService
from ..services.admin import AdminService
from .auth import verify_admin_access

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="Vehicle Asset API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request/response
class VerifyRequest(BaseModel):
    name: str
    id_digits: str

class PickupRequest(BaseModel):
    user_id: str
    asset_ids: List[str]

class ReturnRequest(BaseModel):
    user_id: str
    asset_ids: Optional[List[str]] = None
    asset_id: Optional[str] = None

class ActiveLoan(BaseModel):
    identifier: str
    type: str
    user: str
    timestamp: str

class LoanHistoryRecord(BaseModel):
    identifier: str
    type: str
    user_name: str
    loan_time: str
    return_time: Optional[str] = None

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Vehicle Asset API is running"}

@app.post("/verify")
def verify_user(req: VerifyRequest, db: Session = Depends(get_db)):
    service = VerificationService(db)
    result = service.verify_user(req.name, req.id_digits)
    if not result["success"]:
        raise HTTPException(status_code=401, detail=result["message"])
    return result

@app.get("/assets")
def list_assets(type: str = "all", db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.list_assets(asset_type=type)

@app.get("/assets/loans", response_model=List[ActiveLoan])
def list_active_loans(db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.list_active_loans()

@app.get("/assets/loan-records", response_model=List[LoanHistoryRecord])
def list_loan_records(limit: int = 200, db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.list_loan_records(limit=limit)

@app.get("/assets/identifiers", response_model=List[str])
def list_identifiers(db: Session = Depends(get_db)):
    service = AssetService(db)
    return service.list_all_identifiers()

@app.post("/pickup")
def pickup_assets(req: PickupRequest, db: Session = Depends(get_db)):
    service = AssetService(db)
    result = service.pickup(req.user_id, req.asset_ids)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/return")
def return_assets(req: ReturnRequest, db: Session = Depends(get_db)):
    service = AssetService(db)
    asset_ids = req.asset_ids or ([req.asset_id] if req.asset_id else [])
    if not asset_ids:
        raise HTTPException(status_code=400, detail="No asset IDs provided")
    result = service.return_assets(req.user_id, asset_ids)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# Admin Endpoints
admin_router = APIRouter(prefix="/admin", dependencies=[Depends(verify_admin_access)])

class AddAssetRequest(BaseModel):
    type: str
    identifier: str

class AddUserRequest(BaseModel):
    name: str
    id_last4: str

@admin_router.post("/assets")
def admin_add_asset(req: AddAssetRequest, db: Session = Depends(get_db)):
    service = AdminService(db)
    from ..models import AssetType
    asset_type = AssetType.KEY if req.type.upper() == "KEY" else AssetType.GAS_CARD
    asset = service.add_asset(asset_type, req.identifier)
    return {"id": str(asset.id), "identifier": asset.identifier}

class UpdateAssetRequest(BaseModel):
    identifier: Optional[str] = None
    type: Optional[str] = None
    maintenance_date: Optional[str] = None
    maintenance_mileage: Optional[int] = None
    inspection_date: Optional[str] = None
    insurance_date: Optional[str] = None

@admin_router.patch("/assets/{asset_id}")
def admin_update_asset(asset_id: str, req: UpdateAssetRequest, db: Session = Depends(get_db)):
    service = AdminService(db)
    from ..models import AssetType
    from datetime import datetime
    asset_type = None
    if req.type:
        asset_type = AssetType.KEY if req.type.upper() == "KEY" else AssetType.GAS_CARD
        
    def parse_dt(dt_str):
        if dt_str:
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return None

    asset = service.update_asset(
        asset_id, 
        identifier=req.identifier, 
        type=asset_type,
        maintenance_date=parse_dt(req.maintenance_date),
        maintenance_mileage=req.maintenance_mileage,
        inspection_date=parse_dt(req.inspection_date),
        insurance_date=parse_dt(req.insurance_date)
    )
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    res = {"id": str(asset.id), "identifier": asset.identifier, "type": asset.type.value}
    if asset.type.value == "KEY":
        def safe_iso(dt):
            if dt and hasattr(dt, 'isoformat'):
                return dt.isoformat() + "Z"
            return dt
            
        res["maintenance_date"] = safe_iso(asset.maintenance_date)
        res["maintenance_mileage"] = asset.maintenance_mileage
        res["inspection_date"] = safe_iso(asset.inspection_date)
        res["insurance_date"] = safe_iso(asset.insurance_date)
    return res

@admin_router.delete("/assets/{asset_id}")
def admin_delete_asset(asset_id: str, db: Session = Depends(get_db)):
    service = AdminService(db)
    if not service.delete_asset(asset_id):
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"message": "Asset deleted"}

@admin_router.get("/users")
def admin_list_users(db: Session = Depends(get_db)):
    service = AdminService(db)
    users = service.list_users()
    return [{"id": str(u.id), "name": u.name, "id_last4": u.id_last4, "status": u.status.value} for u in users]

@admin_router.get("/otp/count")
def admin_get_otp_count(db: Session = Depends(get_db)):
    service = AdminService(db)
    count = service.get_otp_count()
    return {"count": count}

class AddOTPRequest(BaseModel):
    password: str

@admin_router.post("/otp/single")
def admin_add_single_otp(req: AddOTPRequest, db: Session = Depends(get_db)):
    service = AdminService(db)
    try:
        result = service.add_single_otp(req.password)
        return {"message": "OTP added successfully", "total_pool": result["total_pool"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@admin_router.post("/otp/batch")
def admin_batch_upload_otp(file: UploadFile = File(...), db: Session = Depends(get_db)):
    service = AdminService(db)
    content = file.file.read().decode("utf-8")
    
    tokens = []
    for line in content.splitlines():
        for t in line.split(','):
            cleaned = t.strip()
            if cleaned:
                tokens.append(cleaned)
                
    for token in tokens:
        if not (len(token) == 8 and token.isdigit()):
            raise HTTPException(status_code=400, detail="文件中包含无效的 OTP 格式")
            
    try:
        result = service.seed_otps(tokens)
        return {"added": result["added"], "skipped": result["skipped"], "total_pool": result["total_pool"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@admin_router.post("/users")
def admin_add_user(req: AddUserRequest, db: Session = Depends(get_db)):
    service = AdminService(db)
    user = service.add_user(req.name, req.id_last4)
    return {"id": str(user.id), "name": user.name}

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    id_last4: Optional[str] = None

@admin_router.patch("/users/{user_id}")
def admin_update_user(user_id: str, req: UpdateUserRequest, db: Session = Depends(get_db)):
    service = AdminService(db)
    user = service.update_user(user_id, name=req.name, id_last4=req.id_last4)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": str(user.id), "name": user.name}

@admin_router.delete("/users/{user_id}")
def admin_delete_user(user_id: str, db: Session = Depends(get_db)):
    service = AdminService(db)
    if not service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

app.include_router(admin_router)
