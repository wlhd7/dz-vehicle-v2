import pytest
from typer.testing import CliRunner
import json
from datetime import datetime, timedelta
from vehicle_asset_lib.cli import app
from vehicle_asset_lib.models import Base, Asset, AssetType, AssetStatus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vehicle_asset_lib.db import SessionLocal

runner = CliRunner()

@pytest.fixture
def mock_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    # Overwrite the db for CLI testing
    import vehicle_asset_lib.cli
    vehicle_asset_lib.cli.SessionLocal = Session
    
    session = Session()
    yield session
    session.close()

def test_notify_admins_no_warnings(mock_db, monkeypatch):
    monkeypatch.setenv("ADMIN_NOTIFICATION_EMAIL", "test@example.com")
    result = runner.invoke(app, ["notify-admins"])
    assert result.exit_code == 0
    assert "No vehicle warnings detected. No email sent." in result.stdout

def test_notify_admins_dry_run(mock_db, monkeypatch):
    monkeypatch.setenv("ADMIN_NOTIFICATION_EMAIL", "test@example.com")
    
    now = datetime.utcnow()
    v = Asset(type=AssetType.KEY, identifier="V-001", status=AssetStatus.AVAILABLE,
              maintenance_date=now - timedelta(days=200))
    mock_db.add(v)
    mock_db.commit()

    result = runner.invoke(app, ["notify-admins", "--dry-run"])
    assert result.exit_code == 0
    assert "[DRY RUN]" in result.stdout
    assert "V-001" in result.stdout
    
    # Check JSON output
    result_json = runner.invoke(app, ["notify-admins", "--dry-run", "--json"])
    assert result_json.exit_code == 0
    data = json.loads(result_json.stdout)
    assert len(data) == 1
    assert data[0]["identifier"] == "V-001"

def test_notify_admins_send_email(mock_db, monkeypatch):
    monkeypatch.setenv("ADMIN_NOTIFICATION_EMAIL", "test@example.com")
    # Provide a bad smtp server to ensure it handles failure gracefully or pass depending on implementation
    monkeypatch.setenv("SMTP_SERVER", "localhost")
    monkeypatch.setenv("SMTP_PORT", "1025")
    
    now = datetime.utcnow()
    v = Asset(type=AssetType.KEY, identifier="V-002", status=AssetStatus.AVAILABLE,
              inspection_date=now + timedelta(days=10))
    mock_db.add(v)
    mock_db.commit()

    # The actual send might fail since no real SMTP server is running on 1025
    result = runner.invoke(app, ["notify-admins", "--json"])
    assert result.exit_code == 0
    data = json.loads(result_json := result.stdout)
    assert len(data["alerts"]) == 1
    assert data["alerts"][0]["identifier"] == "V-002"
    # sent will be False due to connection error
    assert data["sent"] is False
