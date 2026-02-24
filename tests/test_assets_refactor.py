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

def test_pickup_limits_fail_two_keys(session):
    user = User(name="John Doe", id_last4="1234")
    asset1 = Asset(type=AssetType.KEY, identifier="KEY-1", status=AssetStatus.AVAILABLE)
    asset2 = Asset(type=AssetType.KEY, identifier="KEY-2", status=AssetStatus.AVAILABLE)
    otp = OTPPool(password="123456", is_used=False)
    session.add_all([user, asset1, asset2, otp])
    session.commit()
    
    service = AssetService(session)
    # Attempting to pickup two keys at once should fail
    result = service.pickup(str(user.id), [str(asset1.id), str(asset2.id)])
    
    assert result["success"] is False
    assert "more than one vehicle" in result["message"]

def test_pickup_limits_fail_already_held_key(session):
    user = User(name="John Doe", id_last4="1234")
    session.add(user)
    session.flush()
    # User already holds a key
    asset_held = Asset(type=AssetType.KEY, identifier="HELD-KEY", status=AssetStatus.CHECKED_OUT, current_holder_id=user.id)
    asset_new = Asset(type=AssetType.KEY, identifier="NEW-KEY", status=AssetStatus.AVAILABLE)
    otp = OTPPool(password="123456", is_used=False)
    session.add_all([asset_held, asset_new, otp])
    session.commit()
    
    service = AssetService(session)
    # Attempting to pickup another key should fail
    result = service.pickup(str(user.id), [str(asset_new.id)])
    
    assert result["success"] is False, f"Expected failure, got success: {result}"
    assert "already hold a vehicle" in result["message"]

def test_batch_return_success(session):
    user = User(name="John Doe", id_last4="1234")
    session.add(user)
    session.flush()
    asset1 = Asset(type=AssetType.KEY, identifier="KEY-1", status=AssetStatus.CHECKED_OUT, current_holder_id=user.id)
    asset2 = Asset(type=AssetType.GAS_CARD, identifier="GC-1", status=AssetStatus.CHECKED_OUT, current_holder_id=user.id)
    otp = OTPPool(password="654321", is_used=False)
    session.add_all([asset1, asset2, otp])
    session.commit()
    
    service = AssetService(session)
    # New method return_assets to handle multiple IDs
    result = service.return_assets(str(user.id), [str(asset1.id), str(asset2.id)])
    
    assert result["success"] is True, f"Expected success, got failure: {result.get('message')}"
    assert result["otp"] == "654321"
    
    session.refresh(asset1)
    session.refresh(asset2)
    assert asset1.status == AssetStatus.AVAILABLE
    assert asset2.status == AssetStatus.AVAILABLE
    assert asset1.current_holder_id is None
    assert asset2.current_holder_id is None
