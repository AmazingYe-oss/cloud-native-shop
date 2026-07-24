# Cloud Native Shop — 应用代码仓库

云原生电商微服务系统的应用代码，包含 4 个微服务、Dockerfile、K8s 清单和 CI 流水线。

## 项目结构

```
├── services/                    # 微服务源码
│   ├── frontend/                # 前端（Nginx 静态页面）
│   ├── user-service/            # 用户服务（FastAPI）
│   ├── product-service/         # 商品服务（FastAPI）
│   └── order-service/           # 订单服务（FastAPI）
├── deploy/
│   ├── docker/                  # 4 个 Dockerfile
│   └── k8s/                     # K8s Deployment + Service 清单
├── .github/workflows/
│   └── ci.yml                   # GitHub Actions CI 流水线
├── docker-compose.yaml          # 本地开发一键启动
└── README.md
```

## 微服务

| 服务 | 端口 | 技术栈 | 说明 |
|------|------|--------|------|
| frontend | 80 | Nginx | 静态前端页面 |
| user-service | 8000 | FastAPI | 用户管理 |
| product-service | 8000 | FastAPI | 商品管理 |
| order-service | 8000 | FastAPI | 订单管理 |

## 本地开发

```bash
docker-compose up -d
# 前端：http://localhost:8080
# user-service：http://localhost:8001/docs
# product-service：http://localhost:8002/docs
# order-service：http://localhost:8003/docs
```

## CI 流水线

GitHub Actions 自动执行三阶段：

1. **lint-and-test** — ruff 代码检查 + pytest 单元测试（并行矩阵）
2. **build-and-push** — 构建 Docker 镜像推送到阿里云 ACR（仅 main 分支 push 触发）
3. **update-gitops** — 更新 GitOps 仓库的镜像 tag（commit SHA 短格式）

## 镜像仓库

阿里云 ACR 个人版：`crpi-he7mqvhihpnvi08o.cn-shanghai.personal.cr.aliyuncs.com/cloud-native-shop1/<服务名>`
