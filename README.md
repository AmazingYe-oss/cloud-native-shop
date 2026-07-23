# Cloud Native Shop

云原生电商微服务系统，完整覆盖 DevOps 全流程：容器化 → Kubernetes 编排 → CI/CD → GitOps → 可观测性 → 故障演练。

## 系统架构

```
                    ┌─────────────────┐
                    │   Frontend      │
                    │   (Nginx)       │
                    │   :80           │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼───┐  ┌──────▼─────┐  ┌────▼──────────┐
     │user-service│  │product-svc │  │ order-service  │
     │  FastAPI   │  │  FastAPI   │  │   FastAPI      │
     │  :8000     │  │  :8000     │  │   :8000        │
     └────────────┘  └────────────┘  └────────────────┘
```

## 微服务列表

| 服务 | 端口 | 说明 |
|------|------|------|
| `frontend` | 80 | Nginx 静态前端 |
| `user-service` | 8000 | 用户服务（FastAPI） |
| `product-service` | 8000 | 商品服务（FastAPI） |
| `order-service` | 8000 | 订单服务（FastAPI） |

## 技术栈

| 领域 | 技术选型 |
|------|----------|
| 业务开发 | Python FastAPI、原生前端 |
| 容器化 | Docker、Docker Compose |
| 编排调度 | Kubernetes |
| 云平台 | 阿里云 ACK、ACR、VPC |
| 基础设施 | Terraform → [cloud-native-infra](https://github.com/AmazingYe-oss/cloud-native-infra) |
| CI 流水线 | GitHub Actions |
| GitOps | ArgoCD → [cloud-native-shop-gitops](https://github.com/AmazingYe-oss/cloud-native-shop-gitops) |
| 可观测性 | Prometheus、Grafana、Loki、Alertmanager |
| 压测 | k6 |

## 目录结构

```
cloud-native-shop/
├── services/                   # 微服务源码
│   ├── frontend/               # 前端（Nginx + 静态文件）
│   ├── user-service/           # 用户服务
│   ├── product-service/        # 商品服务
│   └── order-service/          # 订单服务
├── deploy/
│   ├── docker/                 # Dockerfile（4 个服务）
│   └── k8s/                    # Kubernetes 清单
│       ├── namespace.yaml
│       ├── *-deployment.yaml
│       └── *-service.yaml
├── .github/workflows/          # GitHub Actions CI 配置
├── scripts/                    # 运维辅助脚本
├── docs/                       # 项目文档
├── docker-compose.yaml         # 本地开发环境
└── README.md
```

## 三个仓库的关系

```
cloud-native-shop          ← 你正在看的：应用代码 + Dockerfile + K8s 清单
    │
    │  CI 构建镜像 → 推送 ACR
    │  CI 更新镜像 tag → 提交到 ↓
    │
cloud-native-shop-gitops   ← ArgoCD 监听此仓库，自动同步到 K8s
    │
    │  部署到 ↓
    │
cloud-native-infra         ← Terraform 管理的阿里云基础设施（VPC/ACK/ACR/RAM）
```

**开发流程**：代码提交 → GitHub Actions CI → 构建镜像 → 推 ACR → 更新 GitOps 仓库 → ArgoCD 自动部署

## 本地开发

```bash
# 启动所有服务
docker-compose up -d

# 访问前端
http://localhost:8080

# 各服务 API
http://localhost:8001  # user-service
http://localhost:8002  # product-service
http://localhost:8003  # order-service
```

## Kubernetes 部署

```bash
# 创建命名空间
kubectl apply -f deploy/k8s/namespace.yaml

# 部署所有服务
kubectl apply -f deploy/k8s/

# 验证
kubectl -n cloud-native-shop get pods
```

## 镜像规范

- Registry: `registry.cn-shanghai.aliyuncs.com/cloud-native-shop/<服务名>`
- 命名空间: `cloud-native-shop`
- 容器端口: 前端 `80`，后端统一 `8000`
- 健康检查: 所有服务暴露 `/health` 端点

## 项目进度

| Day | 内容 | 状态 |
|-----|------|------|
| 1 | 项目初始化、仓库搭建、微服务基础代码 | ✅ |
| 2 | 容器化 + 本地 K8s 部署验证 | ✅ |
| 3 | Terraform 编排阿里云基础设施 | ✅ |
| 4 | GitHub Actions CI 流水线 | 📋 进行中 |
| 5 | ArgoCD GitOps 声明式交付 | 📋 待开始 |
| 6 | 可观测性（Prometheus + Grafana + Loki） | 📋 待开始 |
| 7 | k6 压测与故障演练 | 📋 待开始 |

## License

MIT
