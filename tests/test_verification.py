import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vehicle_asset_lib.models import Base, User, UserStatus
from vehicle_asset_lib.services.verification import VerificationService

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_verify_user_success(session):
    user = User(name="John Doe", id_last4="1234", status=UserStatus.ACTIVE)
    session.add(user)
    session.commit()
    
    service = VerificationService(session)
    result = service.verify_user("John Doe", "1234")
    
    assert result["success"] is True
    assert result["user_id"] == str(user.id)
    assert result["message"] == "Authenticated"

def test_verify_user_fail_wrong_digits(session):
    user = User(name="John Doe", id_last4="1234", status=UserStatus.ACTIVE)
    session.add(user)
    session.commit()
    
    service = VerificationService(session)
    result = service.verify_user("John Doe", "9999")
    
    assert result["success"] is False
    assert result["message"] == "Invalid name or ID digits"

def test_verify_user_fail_inactive(session):
    user = User(name="John Doe", id_last4="1234", status=UserStatus.INACTIVE)
    session.add(user)
    session.commit()
    
    service = VerificationService(session)
    result = service.verify_user("John Doe", "1234")
    
    assert result["success"] is False
    assert result["message"] == "User account is inactive"

def test_verify_user_not_found(session):
    service = VerificationService(session)
    result = service.verify_user("Unknown User", "1234")
    
    assert result["success"] is False
    assert result["message"] == "Invalid name or ID digits"
