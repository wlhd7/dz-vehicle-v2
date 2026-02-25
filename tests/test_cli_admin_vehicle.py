import pytest
from typer.testing import CliRunner
import json
from datetime import datetime, timedelta
from vehicle_asset_lib.cli import app
from vehicle_asset_lib.models import Base, Asset, AssetType, AssetStatus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import vehicle_asset_lib.cli

runner = CliRunner()

@pytest.fixture
def mock_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    # Overwrite the db for CLI testing
    monkeypatch.setattr(vehicle_asset_lib.cli, "SessionLocal", Session)
    
    session = Session()
    yield session
    session.close()

def test_cli_update_asset_vehicle_info(mock_db, monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET", "test-secret")
    
    # Create initial asset
    asset = Asset(type=AssetType.KEY, identifier="V-OLD")
    mock_db.add(asset)
    mock_db.commit()
    asset_id = str(asset.id)

    # Update using CLI
    now = datetime.utcnow().replace(microsecond=0)
    m_date = (now - timedelta(days=5)).isoformat()
    insp_date = (now + timedelta(days=30)).isoformat()
    insu_date = (now + timedelta(days=60)).isoformat()
    
    result = runner.invoke(app, [
        "admin", "update-asset", asset_id,
        "--maintenance-date", m_date,
        "--maintenance-mileage", "12345",
        "--inspection-date", insp_date,
        "--insurance-date", insu_date
    ])
    
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["identifier"] == "V-OLD"
    assert data["maintenance_date"].startswith(m_date)
    assert data["maintenance_mileage"] == 12345
    assert data["inspection_date"].startswith(insp_date)
    assert data["insurance_date"].startswith(insu_date)

    # Verify in DB
    mock_db.expire_all()
    updated_asset = mock_db.query(Asset).filter(Asset.id == asset.id).first()
    assert updated_asset.maintenance_mileage == 12345
    assert updated_asset.maintenance_date.isoformat().startswith(m_date)

def test_cli_update_asset_partial_info(mock_db, monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET", "test-secret")
    
    # Create initial asset with some info
    now = datetime.utcnow().replace(microsecond=0)
    asset = Asset(
        type=AssetType.KEY, 
        identifier="V-PARTIAL",
        maintenance_mileage=5000,
        maintenance_date=now - timedelta(days=10)
    )
    mock_db.add(asset)
    mock_db.commit()
    asset_id = str(asset.id)

    # Update only mileage
    result = runner.invoke(app, [
        "admin", "update-asset", asset_id,
        "--maintenance-mileage", "6000"
    ])
    
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["maintenance_mileage"] == 6000
    # Date should remain same
    assert data["maintenance_date"].startswith((now - timedelta(days=10)).isoformat())

    # Verify in DB
    mock_db.expire_all()
    updated_asset = mock_db.query(Asset).filter(Asset.id == asset.id).first()
    assert updated_asset.maintenance_mileage == 6000
    assert updated_asset.maintenance_date == (now - timedelta(days=10))

def test_cli_list_vehicle_info(mock_db, monkeypatch):
    # Create an asset with vehicle info
    now = datetime.utcnow().replace(microsecond=0)
    asset = Asset(
        type=AssetType.KEY, 
        identifier="V-LIST",
        maintenance_mileage=7000,
        maintenance_date=now - timedelta(days=20)
    )
    mock_db.add(asset)
    mock_db.commit()

    result = runner.invoke(app, ["list", "--type", "KEY"])
    
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data) >= 1
    found = False
    for item in data:
        if item["identifier"] == "V-LIST":
            assert item["maintenance_mileage"] == 7000
            assert item["maintenance_date"].startswith((now - timedelta(days=20)).isoformat())
            found = True
            break
    assert found is True

def test_cli_add_asset_vehicle_info(mock_db, monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET", "test-secret")
    
    now = datetime.utcnow().replace(microsecond=0)
    m_date = now.isoformat()
    
    result = runner.invoke(app, [
        "admin", "add-asset", "KEY", "V-NEW",
        "--maintenance-date", m_date,
        "--maintenance-mileage", "100"
    ])
    
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["identifier"] == "V-NEW"
    assert data["maintenance_mileage"] == 100
    assert data["maintenance_date"].startswith(m_date)

    # Verify in DB
    mock_db.expire_all()
    asset = mock_db.query(Asset).filter(Asset.identifier == "V-NEW").first()
    assert asset.maintenance_mileage == 100
    assert asset.maintenance_date.isoformat().startswith(m_date)
