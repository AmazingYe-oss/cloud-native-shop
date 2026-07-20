# Cloud Native Shop

基于云原生技术栈的电商微服务系统，完整覆盖 DevOps 全流程：容器化、Kubernetes 编排、CI/CD、GitOps、可观测性与故障演练。


## 项目背景

本项目为 DevOps 实战项目，目标是从零搭建一套符合企业级规范的云原生持续交付平台，串联 AWS、Kubernetes、Terraform、Argo CD 等技术栈，形成可持续迭代的云原生应用交付体系。


## 技术栈

| 领域 | 技术选型 |
|---|---|
| 业务开发 | Python FastAPI、原生前端 |
| 容器化 | Docker、Docker Compose |
| 编排调度 | Kubernetes、Helm |
| 云平台 | AWS EKS、ECR、VPC |
| 基础设施代码 | Terraform |
| CI 流水线 | GitHub Actions |
| GitOps 交付 | Argo CD |
| 可观测性 | Prometheus、Grafana、Loki、Alertmanager |
| 压测工具 | k6 |


## 架构设计

（后续补充完整架构图）


## 目录结构

```text
.
├── .github/workflows/     # GitHub Actions CI 流水线
│
├── services/              # 微服务源码
│
├── deploy/                # 部署配置（Docker、Kubernetes）
│
├── docs/                  # 项目文档
│
├── scripts/               # 运维辅助脚本
│
├── .gitignore
│
└── README.md
```


## 快速开始

（后续补充本地部署步骤）


## 许可证

MIT License
