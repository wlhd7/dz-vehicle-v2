import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vehicle_asset_lib.models import Base, OTPPool
from vehicle_asset_lib.api.main import app, get_db

DB_FILE = "test_admin_otp.db"
DATABASE_URL = f"sqlite:///{DB_FILE}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

@pytest.fixture(autouse=True)
def setup_env():
    os.environ["ADMIN_SECRET"] = "test_secret"
    yield
    if "ADMIN_SECRET" in os.environ:
        del os.environ["ADMIN_SECRET"]

def test_get_otp_count_unauthorized():
    response = client.get("/admin/otp/count")
    assert response.status_code == 403

def test_get_otp_count_success():
    db = TestingSessionLocal()
    db.add(OTPPool(password="11111111", is_used=False))
    db.add(OTPPool(password="22222222", is_used=False))
    db.add(OTPPool(password="33333333", is_used=True))
    db.commit()
    db.close()

    response = client.get(
        "/admin/otp/count",
        headers={"X-Admin-Secret": "test_secret"}
    )
    
    assert response.status_code == 200
    assert response.json()["count"] == 2

def test_add_single_otp_success():
    response = client.post(
        "/admin/otp/single",
        json={"password": "12345678"},
        headers={"X-Admin-Secret": "test_secret"}
    )
    
    assert response.status_code == 200
    assert response.json()["message"] == "OTP added successfully"
    assert response.json()["total_pool"] == 1

def test_add_single_otp_invalid_format():
    response = client.post(
        "/admin/otp/single",
        json={"password": "123"},
        headers={"X-Admin-Secret": "test_secret"}
    )
    
    assert response.status_code == 400

def test_batch_upload_otp_success(tmp_path):
    file_path = tmp_path / "otps.txt"
    file_path.write_text("11111111\n22222222\n33333333")
    
    with open(file_path, "rb") as f:
        response = client.post(
            "/admin/otp/batch",
            files={"file": f},
            headers={"X-Admin-Secret": "test_secret"}
        )
    
    assert response.status_code == 200
    assert response.json()["added"] == 3
    assert response.json()["total_pool"] == 3

def test_batch_upload_otp_atomic_failure(tmp_path):
    file_path = tmp_path / "otps.txt"
    file_path.write_text("11111111\n22222\n33333333")
    
    with open(file_path, "rb") as f:
        response = client.post(
            "/admin/otp/batch",
            files={"file": f},
            headers={"X-Admin-Secret": "test_secret"}
        )
    
    assert response.status_code == 400
    assert "无效的 OTP 格式" in response.json()["detail"]
    
    # Check that nothing was added
    db = TestingSessionLocal()
    assert db.query(OTPPool).count() == 0
    db.close()

def test_batch_upload_otp_performance_500(tmp_path):
    import time
    file_path = tmp_path / "otps_500.txt"
    otps = [f"{i:08d}" for i in range(500)]
    file_path.write_text("\n".join(otps))
    
    start_time = time.time()
    with open(file_path, "rb") as f:
        response = client.post(
            "/admin/otp/batch",
            files={"file": f},
            headers={"X-Admin-Secret": "test_secret"}
        )
    end_time = time.time()
    
    assert response.status_code == 200
    assert response.json()["added"] == 500
    assert (end_time - start_time) < 3.0  # SC-002: under 3 seconds
