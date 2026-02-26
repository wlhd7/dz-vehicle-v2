import os

import httpx


def test_public_root_ui_contract():
    endpoint = os.getenv("PROD_ENDPOINT", "http://127.0.0.1:8081/")
    response = httpx.get(endpoint, timeout=10)

    assert response.status_code == 200
    content_type = response.headers.get("content-type", "")
    assert "text/html" in content_type
