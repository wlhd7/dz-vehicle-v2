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

def test_list_active_loans_sorting(db_session):
    service = AssetService(db_session)
    
    # Create user
    user = User(name="testuser", id_last4="1234")
    db_session.add(user)
    
    # Create OTP
    otp1 = OTPPool(password="123456")
    otp2 = OTPPool(password="654321")
    db_session.add_all([otp1, otp2])
    db_session.commit()
    
    # Create assets
    asset1 = Asset(type=AssetType.KEY, identifier="V001", status=AssetStatus.CHECKED_OUT, current_holder_id=user.id)
    asset2 = Asset(type=AssetType.GAS_CARD, identifier="C001", status=AssetStatus.CHECKED_OUT, current_holder_id=user.id)
    asset3 = Asset(type=AssetType.KEY, identifier="V002", status=AssetStatus.AVAILABLE)
    db_session.add_all([asset1, asset2, asset3])
    db_session.commit()
    
    # Create transaction logs with different timestamps
    now = datetime.utcnow()
    log1 = TransactionLog(user_id=user.id, asset_id=asset1.id, action=TransactionAction.PICKUP, otp_id=otp1.id, timestamp=now - timedelta(minutes=10))
    log2 = TransactionLog(user_id=user.id, asset_id=asset2.id, action=TransactionAction.PICKUP, otp_id=otp2.id, timestamp=now)
    db_session.add_all([log1, log2])
    db_session.commit()
    
    # Call the new method (should fail if not implemented)
    loans = service.list_active_loans()
    
    assert len(loans) == 2
    # Newest should be first (asset2/C001)
    assert loans[0]["identifier"] == "C001"
    assert loans[0]["user"] == "testuser"
    assert loans[1]["identifier"] == "V001"

from typer.testing import CliRunner
from vehicle_asset_lib.cli import app as cli_app

def test_cli_loans(db_session, monkeypatch):
    # Setup data
    user = User(name="cliuser", id_last4="8888")
    db_session.add(user)
    db_session.commit()
    
    otp = OTPPool(password="111222")
    db_session.add(otp)
    db_session.commit()
    
    asset = Asset(type=AssetType.KEY, identifier="CLI-V1", status=AssetStatus.CHECKED_OUT, current_holder_id=user.id)
    db_session.add(asset)
    db_session.commit()
    
    log = TransactionLog(user_id=user.id, asset_id=asset.id, action=TransactionAction.PICKUP, otp_id=otp.id, timestamp=datetime.utcnow())
    db_session.add(log)
    db_session.commit()
    
    # We need to monkeypatch SessionLocal in cli.py to use our db_session
    import vehicle_asset_lib.cli
    monkeypatch.setattr(vehicle_asset_lib.cli, "SessionLocal", lambda: db_session)
    
    runner = CliRunner()
    result = runner.invoke(cli_app, ["loans"])
    
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data) == 1
    assert data[0]["identifier"] == "CLI-V1"

import json
