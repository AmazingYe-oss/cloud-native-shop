import time
import logging
from pythonjsonlogger import jsonlogger
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

# ========== 1. 结构化日志配置 ==========
logger = logging.getLogger("user-service")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s %(path)s %(status_code)s %(latency)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# ========== 2. Prometheus 指标定义 ==========
REQUEST_COUNT = Counter(
    "user_service_requests_total",
    "Total number of requests to user service",
    ["method", "endpoint", "status_code"]
)
REQUEST_LATENCY = Histogram(
    "user_service_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"]
)

# ========== 3. 模拟内存数据库 ==========
# 业务极简，重点在 DevOps 特性，后续阶段替换为 PostgreSQL
mock_users = [
    {"id": 1, "name": "张三", "email": "zhangsan@example.com"},
    {"id": 2, "name": "李四", "email": "lisi@example.com"},
    {"id": 3, "name": "王五", "email": "wangwu@example.com"},
]

# ========== 4. FastAPI 应用 ==========
app = FastAPI(title="User Service")

# 中间件：统计请求指标 + 结构化日志
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time

    # 记录指标
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(latency)

    # 记录结构化访问日志
    logger.info(
        "request handled",
        extra={
            "path": request.url.path,
            "status_code": response.status_code,
            "latency": round(latency, 4)
        }
    )
    return response

# ========== 5. 核心接口 ==========

# 健康检查接口 - K8s 探针专用
@app.get("/health", summary="健康检查")
async def health_check():
    return {"status": "ok", "service": "user-service"}

# Prometheus 指标接口
@app.get("/metrics", summary="Prometheus 指标")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# 业务接口：获取所有用户
@app.get("/users", summary="获取用户列表")
async def get_users():
    return {"code": 0, "data": mock_users}

# 业务接口：根据ID获取用户
@app.get("/users/{user_id}", summary="根据ID获取用户")
async def get_user(user_id: int):
    user = next((u for u in mock_users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"code": 0, "data": user}