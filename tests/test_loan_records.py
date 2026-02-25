import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vehicle_asset_lib.models import Base, Asset, User, AssetType, AssetStatus, TransactionLog, TransactionAction, OTPPool
from vehicle_asset_lib.services.assets import AssetService
from datetime import datetime, timedelta

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_list_loan_records_pairing(db_session):
    service = AssetService(db_session)
    
    # Create user
    user = User(name="testuser", id_last4="1234")
    db_session.add(user)
    
    # Create OTPs
    otp1 = OTPPool(password="111111")
    otp2 = OTPPool(password="222222")
    db_session.add_all([otp1, otp2])
    db_session.commit()
    
    # Create assets
    asset1 = Asset(type=AssetType.KEY, identifier="V001")
    asset2 = Asset(type=AssetType.GAS_CARD, identifier="C001")
    db_session.add_all([asset1, asset2])
    db_session.commit()
    
    # Scenario: asset1 picked up and returned. asset2 picked up and still out.
    now = datetime.utcnow()
    
    # Asset 1 history
    pickup1 = TransactionLog(user_id=user.id, asset_id=asset1.id, action=TransactionAction.PICKUP, otp_id=otp1.id, timestamp=now - timedelta(hours=2))
    return1 = TransactionLog(user_id=user.id, asset_id=asset1.id, action=TransactionAction.RETURN, otp_id=otp2.id, timestamp=now - timedelta(hours=1))
    
    # Asset 2 history
    pickup2 = TransactionLog(user_id=user.id, asset_id=asset2.id, action=TransactionAction.PICKUP, otp_id=otp1.id, timestamp=now)
    
    db_session.add_all([pickup1, return1, pickup2])
    db_session.commit()
    
    # Call the method
    records = service.list_loan_records()
    
    assert len(records) == 2
    
    # Sort order: newest pickup first (Asset 2)
    assert records[0]["identifier"] == "C001"
    assert records[0]["return_time"] is None
    assert records[0]["user_name"] == "testuser"
    
    # Asset 1 record
    assert records[1]["identifier"] == "V001"
    assert records[1]["return_time"] is not None
    # Check that return time is exactly what we set
    assert records[1]["return_time"] == (now - timedelta(hours=1)).isoformat() + "Z"

from typer.testing import CliRunner
from vehicle_asset_lib.cli import app as cli_app
import json

def test_cli_loan_records(db_session, monkeypatch):
    # Setup data
    user = User(name="cliuser", id_last4="8888")
    db_session.add(user)
    db_session.commit()
    
    otp = OTPPool(password="111222")
    db_session.add(otp)
    db_session.commit()
    
    asset = Asset(type=AssetType.KEY, identifier="CLI-V1")
    db_session.add(asset)
    db_session.commit()
    
    now = datetime.utcnow()
    log = TransactionLog(user_id=user.id, asset_id=asset.id, action=TransactionAction.PICKUP, otp_id=otp.id, timestamp=now)
    db_session.add(log)
    db_session.commit()
    
    # Monkeypatch SessionLocal
    import vehicle_asset_lib.cli
    monkeypatch.setattr(vehicle_asset_lib.cli, "SessionLocal", lambda: db_session)
    
    runner = CliRunner()
    result = runner.invoke(cli_app, ["loan-records"])
    
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data) == 1
    assert data[0]["identifier"] == "CLI-V1"
    assert data[0]["loan_time"] is not None
    assert data[0]["return_time"] is None
