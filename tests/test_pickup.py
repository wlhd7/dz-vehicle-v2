import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vehicle_asset_lib.models import Base, User, Asset, OTPPool, AssetType, AssetStatus, TransactionLog
from vehicle_asset_lib.services.assets import AssetService

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_pickup_success(session):
    user = User(name="John Doe", id_last4="1234")
    asset1 = Asset(type=AssetType.KEY, identifier="ABC-123", status=AssetStatus.AVAILABLE)
    asset2 = Asset(type=AssetType.GAS_CARD, identifier="987654", status=AssetStatus.AVAILABLE)
    otp = OTPPool(password="998877", is_used=False)
    session.add_all([user, asset1, asset2, otp])
    session.commit()
    
    service = AssetService(session)
    result = service.pickup(str(user.id), [str(asset1.id), str(asset2.id)])
    
    assert result["success"] is True
    assert result["otp"] == "998877"
    assert sorted(result["assets"]) == sorted(["ABC-123", "987654"])
    
    # Check states
    session.refresh(asset1)
    session.refresh(asset2)
    session.refresh(otp)
    
    assert asset1.status == AssetStatus.CHECKED_OUT
    assert asset1.current_holder_id == user.id
    assert asset2.status == AssetStatus.CHECKED_OUT
    assert asset2.current_holder_id == user.id
    assert otp.is_used is True
    
    logs = session.query(TransactionLog).all()
    assert len(logs) == 2

def test_pickup_fail_asset_already_checked_out(session):
    user = User(name="John Doe", id_last4="1234")
    user2 = User(name="Jane Smith", id_last4="5678")
    asset = Asset(type=AssetType.KEY, identifier="ABC-123", status=AssetStatus.CHECKED_OUT, current_holder_id=user2.id)
    otp = OTPPool(password="998877", is_used=False)
    session.add_all([user, user2, asset, otp])
    session.commit()
    
    service = AssetService(session)
    result = service.pickup(str(user.id), [str(asset.id)])
    
    assert result["success"] is False
    assert "already checked out" in result["message"]

def test_pickup_fail_otp_exhaustion(session):
    user = User(name="John Doe", id_last4="1234")
    asset = Asset(type=AssetType.KEY, identifier="ABC-123", status=AssetStatus.AVAILABLE)
    # No available OTPs
    session.add_all([user, asset])
    session.commit()
    
    service = AssetService(session)
    result = service.pickup(str(user.id), [str(asset.id)])
    
    assert result["success"] is False
    assert "No codes available" in result["message"]
