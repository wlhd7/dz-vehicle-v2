import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vehicle_asset_lib.models import Base, User, Asset, OTPPool, TransactionLog, UserStatus, AssetType, AssetStatus, TransactionAction

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_user(session):
    user = User(name="John Doe", id_last4="1234", status=UserStatus.ACTIVE)
    session.add(user)
    session.commit()
    
    assert user.id is not None
    assert user.name == "John Doe"
    assert user.id_last4 == "1234"
    assert user.status == UserStatus.ACTIVE

def test_create_asset(session):
    asset = Asset(type=AssetType.KEY, identifier="ABC-123", status=AssetStatus.AVAILABLE)
    session.add(asset)
    session.commit()
    
    assert asset.id is not None
    assert asset.identifier == "ABC-123"
    assert asset.status == AssetStatus.AVAILABLE

def test_create_otp(session):
    otp = OTPPool(password="998877", is_used=False)
    session.add(otp)
    session.commit()
    
    assert otp.id is not None
    assert otp.password == "998877"
    assert otp.is_used is False

def test_transaction_log(session):
    user = User(name="John Doe", id_last4="1234")
    asset = Asset(type=AssetType.KEY, identifier="ABC-123")
    otp = OTPPool(password="998877")
    session.add_all([user, asset, otp])
    session.commit()
    
    log = TransactionLog(user_id=user.id, asset_id=asset.id, action=TransactionAction.PICKUP, otp_id=otp.id)
    session.add(log)
    session.commit()
    
    assert log.id is not None
    assert log.user_id == user.id
    assert log.asset_id == asset.id
    assert log.otp_id == otp.id
