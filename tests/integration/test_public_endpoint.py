import os

import httpx


def test_public_endpoint_reachability():
    endpoint = os.getenv("PROD_ENDPOINT", "http://127.0.0.1:8081/")
    response = httpx.get(endpoint, timeout=10)

    assert response.status_code == 200
    assert response.text.strip() != ""
