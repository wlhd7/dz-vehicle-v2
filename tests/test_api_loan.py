import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vehicle_asset_lib.models import Base, Asset, User, AssetType, AssetStatus, TransactionLog, TransactionAction, OTPPool
from vehicle_asset_lib.api.main import app, get_db
from datetime import datetime, timedelta

import os

# Setup file-based database for testing to avoid in-memory sharing issues
DB_FILE = "test_loan_api.db"
DATABASE_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    Base.metadata.create_all(bind=engine)
    yield
    # Dispose engine to close all connections
    engine.dispose()
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

def test_api_list_active_loans():
    db = TestingSessionLocal()
    
    # Setup data
    user = User(name="apiuser", id_last4="9999")
    db.add(user)
    db.flush()
    
    otp = OTPPool(password="111111")
    db.add(otp)
    db.flush()
    
    asset = Asset(type=AssetType.KEY, identifier="API-V1", status=AssetStatus.CHECKED_OUT, current_holder_id=user.id)
    db.add(asset)
    db.flush()
    
    log = TransactionLog(user_id=user.id, asset_id=asset.id, action=TransactionAction.PICKUP, otp_id=otp.id, timestamp=datetime.utcnow())
    db.add(log)
    db.commit()
    
    response = client.get("/assets/loans")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["identifier"] == "API-V1"
    assert data[0]["user"] == "apiuser"

def test_api_list_active_loans_empty():
    response = client.get("/assets/loans")
    assert response.status_code == 200
    assert response.json() == []

def test_api_list_loan_records():
    db = TestingSessionLocal()
    user = User(name="historyuser", id_last4="1111")
    db.add(user)
    db.flush()
    
    otp = OTPPool(password="111111")
    db.add(otp)
    db.flush()
    
    asset = Asset(type=AssetType.KEY, identifier="HIST-V1")
    db.add(asset)
    db.flush()
    
    # Pickup
    log = TransactionLog(user_id=user.id, asset_id=asset.id, action=TransactionAction.PICKUP, otp_id=otp.id, timestamp=datetime.utcnow())
    db.add(log)
    db.commit()
    
    response = client.get("/assets/loan-records")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["identifier"] == "HIST-V1"
    assert data[0]["return_time"] is None

def test_api_list_identifiers():
    db = TestingSessionLocal()
    asset1 = Asset(type=AssetType.KEY, identifier="ID-V1")
    asset2 = Asset(type=AssetType.GAS_CARD, identifier="ID-C1")
    db.add_all([asset1, asset2])
    db.commit()
    
    response = client.get("/assets/identifiers")
    assert response.status_code == 200
    data = response.json()
    assert "ID-V1" in data
    assert "ID-C1" in data
