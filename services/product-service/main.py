import logging
import time

from fastapi import FastAPI, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pythonjsonlogger import jsonlogger
from starlette.responses import Response

# 日志配置
logger = logging.getLogger("product-service")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s %(path)s %(status_code)s %(latency)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Prometheus 指标
REQUEST_COUNT = Counter(
    "product_service_requests_total",
    "Total number of requests to product service",
    ["method", "endpoint", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "product_service_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
)

# 模拟商品数据
mock_products = [
    {"id": 1, "name": "机械键盘", "price": 299, "stock": 100},
    {"id": 2, "name": "无线鼠标", "price": 99, "stock": 200},
    {"id": 3, "name": "显示器支架", "price": 199, "stock": 50},
]

app = FastAPI(title="Product Service")


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
    return {"status": "ok", "service": "product-service"}


# 指标接口
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# 获取所有商品
@app.get("/products")
async def get_products():
    return {"code": 0, "data": mock_products}


# 根据ID获取商品
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    product = next((p for p in mock_products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"code": 0, "data": product}
