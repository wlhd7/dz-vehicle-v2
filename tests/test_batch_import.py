import pytest
import json
import os
from typer.testing import CliRunner
from vehicle_asset_lib.cli import app
from vehicle_asset_lib.db import Base
from vehicle_asset_lib.models import User, OTPPool

runner = CliRunner()

@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from vehicle_asset_lib import db as db_module
    from vehicle_asset_lib import cli as cli_module
    
    # Use in-memory database
    test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    # Patch the module-level objects
    monkeypatch.setattr(db_module, "engine", test_engine)
    monkeypatch.setattr(db_module, "SessionLocal", TestSessionLocal)
    monkeypatch.setattr(cli_module, "SessionLocal", TestSessionLocal)
    
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

def test_batch_add_users_success(tmp_path):
    # Setup test file
    users_file = tmp_path / "users.txt"
    users_file.write_text("Alice,1234
Bob,5678,Charlie,9012", encoding="utf-8")
    
    # Run command
    result = runner.invoke(app, ["admin", "batch-add-users", str(users_file)])
    
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["added"] == 3
    assert data["skipped"] == 0
    assert data["total"] == 3
    
    # Verify in DB
    from vehicle_asset_lib.db import SessionLocal
    with SessionLocal() as db:
        users = db.query(User).all()
        assert len(users) == 3
        names = [u.name for u in users]
        assert "Alice" in names
        assert "Bob" in names
        assert "Charlie" in names

def test_batch_add_users_duplicate(tmp_path):
    from vehicle_asset_lib.db import SessionLocal
    # Pre-add Alice
    with SessionLocal() as db:
        db.add(User(name="Alice", id_last4="1234"))
        db.commit()
    
    users_file = tmp_path / "users.txt"
    users_file.write_text("Alice,1234,Bob,5678", encoding="utf-8")
    
    result = runner.invoke(app, ["admin", "batch-add-users", str(users_file)])
    
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["added"] == 1
    assert data["skipped"] == 1
    assert data["total"] == 2

def test_batch_add_users_atomic_failure_odd_tokens(tmp_path):
    users_file = tmp_path / "users.txt"
    users_file.write_text("Alice,1234,Bob", encoding="utf-8")
    
    result = runner.invoke(app, ["admin", "batch-add-users", str(users_file)])
    
    assert result.exit_code == 1
    output = result.stdout + result.stderr
    assert "[Atomic Failure]" in output
    
    # Verify no users added
    from vehicle_asset_lib.db import SessionLocal
    with SessionLocal() as db:
        assert db.query(User).count() == 0

def test_batch_add_users_atomic_failure_invalid_id(tmp_path):
    users_file = tmp_path / "users.txt"
    users_file.write_text("Alice,12345,Bob,5678", encoding="utf-8") # 5 characters
    
    result = runner.invoke(app, ["admin", "batch-add-users", str(users_file)])
    
    assert result.exit_code == 1
    output = result.stdout + result.stderr
    assert "[Atomic Failure]" in output
    assert "Invalid ID_Last4" in output
    
    # Verify no users added
    from vehicle_asset_lib.db import SessionLocal
    with SessionLocal() as db:
        assert db.query(User).count() == 0

def test_seed_otps_file_success(tmp_path):
    otp_file = tmp_path / "otps.txt"
    otp_file.write_text("12345678,87654321
11112222", encoding="utf-8")
    
    result = runner.invoke(app, ["admin", "seed-otps", "--file-path", str(otp_file)])
    
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["added"] == 3
    assert data["skipped"] == 0
    assert data["total_pool"] == 3

def test_seed_otps_file_duplicate(tmp_path):
    from vehicle_asset_lib.db import SessionLocal
    # Pre-add one OTP
    with SessionLocal() as db:
        db.add(OTPPool(password="12345678"))
        db.commit()
    
    otp_file = tmp_path / "otps.txt"
    otp_file.write_text("12345678,87654321", encoding="utf-8")
    
    result = runner.invoke(app, ["admin", "seed-otps", "--file-path", str(otp_file)])
    
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["added"] == 1
    assert data["skipped"] == 1
    assert data["total_pool"] == 2

def test_seed_otps_file_atomic_failure_invalid_format(tmp_path):
    otp_file = tmp_path / "otps.txt"
    otp_file.write_text("12345678,1234567", encoding="utf-8") # 7 digits
    
    result = runner.invoke(app, ["admin", "seed-otps", "--file-path", str(otp_file)])
    
    assert result.exit_code == 1
    output = result.stdout + result.stderr
    assert "[Atomic Failure]" in output
    
    # Verify pool empty
    from vehicle_asset_lib.db import SessionLocal
    with SessionLocal() as db:
        assert db.query(OTPPool).count() == 0
