from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    """健康检查接口返回 200 + status ok"""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_get_products():
    """商品列表接口返回非空数组"""
    resp = client.get("/products")
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0
    assert len(data["data"]) > 0


def test_get_product_found():
    """根据 ID 查询存在的商品"""
    resp = client.get("/products/1")
    assert resp.status_code == 200
    assert resp.json()["data"]["id"] == 1


def test_get_product_not_found():
    """查询不存在的商品返回 404"""
    resp = client.get("/products/999")
    assert resp.status_code == 404
