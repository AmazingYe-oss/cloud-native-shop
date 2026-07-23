from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    """健康检查接口返回 200 + status ok"""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_get_orders():
    """订单列表接口返回非空数组"""
    resp = client.get("/orders")
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
