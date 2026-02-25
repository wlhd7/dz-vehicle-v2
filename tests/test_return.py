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

def test_return_success(session):
    user = User(name="John Doe", id_last4="1234")
    session.add(user)
    session.commit()
    
    asset = Asset(type=AssetType.KEY, identifier="ABC-123", status=AssetStatus.CHECKED_OUT, current_holder_id=user.id)
    otp = OTPPool(password="112233", is_used=False)
    session.add_all([asset, otp])
    session.commit()
    
    service = AssetService(session)
    result = service.return_asset(str(user.id), str(asset.id))
    
    assert result["success"] is True, result.get("message")
    assert result["otp"] == "112233"
    assert "expires_at" in result
    
    # Check states
    session.refresh(asset)
    session.refresh(otp)
    
    assert asset.status == AssetStatus.AVAILABLE
    assert asset.current_holder_id is None
    assert otp.is_used is True
    
    logs = session.query(TransactionLog).all()
    assert len(logs) == 1

def test_return_fail_not_holder(session):
    user = User(name="John Doe", id_last4="1234")
    user2 = User(name="Jane Smith", id_last4="5678")
    session.add_all([user, user2])
    session.commit()
    
    asset = Asset(type=AssetType.KEY, identifier="ABC-123", status=AssetStatus.CHECKED_OUT, current_holder_id=user2.id)
    otp = OTPPool(password="112233", is_used=False)
    session.add_all([asset, otp])
    session.commit()
    
    service = AssetService(session)
    result = service.return_asset(str(user.id), str(asset.id))
    
    assert result["success"] is False
    assert "not the holder" in result["message"]
