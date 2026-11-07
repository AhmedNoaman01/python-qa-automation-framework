"""Start the local demo API once for the full pytest session."""
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests

from clients.api_client import APIClient

ROOT = Path(__file__).resolve().parents[1]

def _free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]

@pytest.fixture(scope="session")
def api_base_url():
    port = int(os.getenv("QA_API_PORT", str(_free_port())))
    base_url = f"http://127.0.0.1:{port}"
    env = os.environ.copy()
    src_path = str(ROOT / "src")
    env["PYTHONPATH"] = src_path + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "demo_api.main:app", "--app-dir", src_path,
         "--host", "127.0.0.1", "--port", str(port), "--log-level", "warning"],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    deadline = time.time() + 12
    ready = False
    while time.time() < deadline:
        if process.poll() is not None:
            raise RuntimeError("Demo API stopped before becoming ready. Check installed dependencies.")
        try:
            response = requests.get(f"{base_url}/health", timeout=0.5)
            if response.status_code == 200:
                ready = True
                break
        except requests.RequestException:
            time.sleep(0.2)
    if not ready:
        process.terminate()
        raise RuntimeError("Demo API did not become ready within 12 seconds.")
    yield base_url
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=3)

@pytest.fixture(scope="session")
def api_client(api_base_url):
    client = APIClient(api_base_url)
    yield client
    client.close()

@pytest.fixture
def make_product(api_client):
    def _make_product(**overrides):
        payload = {"name": "QA Sample Product", "price": 12.5, "stock": 10}
        payload.update(overrides)
        response = api_client.post("/api/products", json=payload)
        assert response.status_code == 201, response.text
        return response.json()
    return _make_product
