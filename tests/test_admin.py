import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vehicle_asset_lib.models import Base, User, Asset, OTPPool, AssetType, UserStatus
from vehicle_asset_lib.services.admin import AdminService
from vehicle_asset_lib.services.monitoring import MonitoringService

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_add_asset(session):
    service = AdminService(session)
    asset = service.add_asset(AssetType.KEY, "XYZ-789")
    
    assert asset.id is not None
    assert asset.identifier == "XYZ-789"

def test_update_asset(session):
    service = AdminService(session)
    asset = service.add_asset(AssetType.KEY, "XYZ-789")
    updated = service.update_asset(str(asset.id), identifier="ABC-123")
    assert updated.identifier == "ABC-123"

def test_delete_asset(session):
    service = AdminService(session)
    asset = service.add_asset(AssetType.KEY, "XYZ-789")
    success = service.delete_asset(str(asset.id))
    assert success is True
    assert service.get_asset(str(asset.id)) is None

def test_add_user_to_whitelist(session):
    service = AdminService(session)
    user = service.add_user("Alice Smith", "5678")
    
    assert user.id is not None
    assert user.name == "Alice Smith"
    assert user.id_last4 == "5678"

def test_update_user(session):
    service = AdminService(session)
    user = service.add_user("Alice Smith", "5678")
    updated = service.update_user(str(user.id), name="Alice Jones")
    assert updated.name == "Alice Jones"

def test_delete_user(session):
    service = AdminService(session)
    user = service.add_user("Alice Smith", "5678")
    success = service.delete_user(str(user.id))
    assert success is True
    assert service.get_user(str(user.id)) is None

def test_list_users(session):
    service = AdminService(session)
    service.add_user("User1", "1111")
    service.add_user("User2", "2222")
    users = service.list_users()
    assert len(users) == 2

def test_seed_otps(session):
    service = AdminService(session)
    # Mocking reading from a file or list
    passwords = ["p1", "p2", "p3"]
    result = service.seed_otps(passwords)
    
    assert result["added"] == 3
    assert session.query(OTPPool).count() == 3

def test_low_otp_threshold(session):
    # Seed 29 OTPs
    for i in range(29):
        session.add(OTPPool(password=f"p{i}", is_used=False))
    session.commit()
    
    monitoring = MonitoringService(session)
    alert = monitoring.check_otp_threshold()
    
    assert alert["triggered"] is True
    assert "Low OTP threshold" in alert["message"]

def test_update_asset_maintenance_and_compliance(session):
    from datetime import datetime, timedelta
    service = AdminService(session)
    asset = service.add_asset(AssetType.KEY, "XYZ-789")
    
    now = datetime.utcnow()
    future_date = now + timedelta(days=365)
    
    updated = service.update_asset(
        str(asset.id), 
        maintenance_date=now,
        maintenance_mileage=15000,
        inspection_date=future_date,
        insurance_date=future_date
    )
    
    assert updated.maintenance_date == now
    assert updated.maintenance_mileage == 15000
    assert updated.inspection_date == future_date
    assert updated.insurance_date == future_date
