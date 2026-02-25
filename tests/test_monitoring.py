import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vehicle_asset_lib.models import Base, Asset, AssetType, AssetStatus
from vehicle_asset_lib.services.monitoring import MonitoringService

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_check_vehicle_alerts(session):
    now = datetime.utcnow()
    # 1. Normal vehicle
    v1 = Asset(type=AssetType.KEY, identifier="V-001", status=AssetStatus.AVAILABLE,
               maintenance_date=now - timedelta(days=30),
               inspection_date=now + timedelta(days=60),
               insurance_date=now + timedelta(days=60))
    # 2. Overdue maintenance (>6 months)
    v2 = Asset(type=AssetType.KEY, identifier="V-002", status=AssetStatus.AVAILABLE,
               maintenance_date=now - timedelta(days=200),
               inspection_date=now + timedelta(days=60),
               insurance_date=now + timedelta(days=60))
    # 3. Inspection expiring within 30 days
    v3 = Asset(type=AssetType.KEY, identifier="V-003", status=AssetStatus.AVAILABLE,
               maintenance_date=now - timedelta(days=30),
               inspection_date=now + timedelta(days=15),
               insurance_date=now + timedelta(days=60))
    # 4. Insurance expiring within 30 days
    v4 = Asset(type=AssetType.KEY, identifier="V-004", status=AssetStatus.AVAILABLE,
               maintenance_date=now - timedelta(days=30),
               inspection_date=now + timedelta(days=60),
               insurance_date=now + timedelta(days=10))

    session.add_all([v1, v2, v3, v4])
    session.commit()

    service = MonitoringService(session)
    alerts = service.check_vehicle_alerts()
    
    assert len(alerts) == 3
    
    # Verify exact alerts
    v2_alerts = [a for a in alerts if a["identifier"] == "V-002"]
    assert len(v2_alerts) == 1
    assert "Maintenance overdue" in v2_alerts[0]["status"]
    
    v3_alerts = [a for a in alerts if a["identifier"] == "V-003"]
    assert len(v3_alerts) == 1
    assert "Inspection expiring" in v3_alerts[0]["status"]
    
    v4_alerts = [a for a in alerts if a["identifier"] == "V-004"]
    assert len(v4_alerts) == 1
    assert "Insurance expiring" in v4_alerts[0]["status"]
