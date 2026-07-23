import time
import uuid
import logging
import requests
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import os

# 日志配置
logger = logging.getLogger("order-service")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s %(path)s %(status_code)s %(latency)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Prometheus 指标
REQUEST_COUNT = Counter(
    "order_service_requests_total",
    "Total number of requests to order service",
    ["method", "endpoint", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "order_service_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
)

# 下游服务地址 - 通过环境变量配置，避免硬编码（云原生十二要素）
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:8001")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8002")

# 模拟订单存储
mock_orders = []

app = FastAPI(title="Order Service")


# 中间件
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
    ).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(
        latency
    )

    logger.info(
        "request handled",
        extra={
            "path": request.url.path,
            "status_code": response.status_code,
            "latency": round(latency, 4),
        },
    )
    return response


# 健康检查
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "order-service"}


# 指标接口
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# 创建订单 - 核心接口，会调用用户和商品服务
@app.post("/orders")
async def create_order(user_id: int, product_id: int, quantity: int = 1):
    # 1. 调用用户服务验证用户存在（设置超时，防止级联阻塞）
    try:
        user_resp = requests.get(f"{USER_SERVICE_URL}/users/{user_id}", timeout=2)
        user_resp.raise_for_status()
        user = user_resp.json()["data"]
    except Exception as e:
        logger.error(f"调用用户服务失败: {str(e)}")
        raise HTTPException(status_code=503, detail="用户服务不可用")

    # 2. 调用商品服务验证商品存在
    try:
        product_resp = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}", timeout=2
        )
        product_resp.raise_for_status()
        product = product_resp.json()["data"]
    except Exception as e:
        logger.error(f"调用商品服务失败: {str(e)}")
        raise HTTPException(status_code=503, detail="商品服务不可用")

    # 3. 生成订单
    order = {
        "order_id": str(uuid.uuid4()),
        "user": user,
        "product": product,
        "quantity": quantity,
        "total_price": product["price"] * quantity,
        "status": "created",
    }
    mock_orders.append(order)
    logger.info(f"订单创建成功: {order['order_id']}")
    return {"code": 0, "data": order}


# 查询订单列表
@app.get("/orders")
async def get_orders():
    return {"code": 0, "data": mock_orders}
