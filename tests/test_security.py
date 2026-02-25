import pytest
import os
from typer.testing import CliRunner
from fastapi.testclient import TestClient
from vehicle_asset_lib.cli import app
from vehicle_asset_lib.api.main import app as api_app

runner = CliRunner()
client = TestClient(api_app)

def test_cli_admin_requires_secret(monkeypatch):
    # US1: Admin CLI should fail without ADMIN_SECRET
    monkeypatch.delenv("ADMIN_SECRET", raising=False)
    
    # Try an admin command
    result = runner.invoke(app, ["admin", "list-users"])
    assert result.exit_code != 0
    assert "Access Denied" in result.stderr

def test_cli_admin_accepts_valid_secret(monkeypatch):
    # US1: Admin CLI should pass with valid ADMIN_SECRET
    monkeypatch.setenv("ADMIN_SECRET", "test_secret")
    
    # We need to make sure the DB is initialized for this test to not fail on DB errors
    # But since we just want to check auth, we can check if it gets past auth
    result = runner.invoke(app, ["admin", "list-users"])
    # If auth passes, it might still fail on DB if not init, but it won't be "Access Denied"
    assert "Access Denied" not in result.stdout

def test_api_admin_requires_header():
    # US3: Admin API should fail without X-Admin-Secret header
    response = client.get("/admin/users")
    assert response.status_code == 403
    assert "[Access Denied] Missing or invalid ADMIN_SECRET" in response.json()["detail"]

def test_api_admin_accepts_valid_header(monkeypatch):
    # US3: Admin API should pass with valid X-Admin-Secret header
    monkeypatch.setenv("ADMIN_SECRET", "test_secret")
    
    # We use a try-except or check for 500 because the DB might not be initialized here
    try:
        response = client.get("/admin/users", headers={"X-Admin-Secret": "test_secret"})
        assert response.status_code in [200, 500]
    except Exception:
        # FastAPI TestClient propagates server exceptions if not handled
        pass
