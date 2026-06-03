## Context

全新技术栈项目，从零搭建。目标用户为抖音内容创作者，需要一个AI驱动的标题优化工具。项目采用多Agent协作开发模式，6个专职Agent分工明确。

## Goals / Non-Goals

**Goals:**
- 提供多维度标题质量评分（吸引力、信息量、可读性、平台适配）
- 集成LLM生成标题优化建议，支持多种优化策略
- 构建直观的Web界面，支持单条和批量优化
- 持久化优化历史，提供数据看板展示趋势
- 完整的CI/CD流水线和Docker容器化部署

**Non-Goals:**
- 不提供视频发布功能（仅标题优化）
- 不直接对接TikTok API获取真实播放数据（预留接口，初期使用模拟数据）
- 不做移动端Native App（仅响应式Web）
- 不支持多用户协作/团队功能（仅单用户模式）

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Nginx (Reverse Proxy)                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌───────────────┐           ┌───────────────┐
│   Frontend    │           │   Backend     │
│  React 18 +   │  REST API │  FastAPI      │
│  TypeScript   │──────────▶│  Python 3.11  │
│  Ant Design   │           │               │
└───────────────┘           └───────┬───────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
      ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
      │  PostgreSQL │       │    Redis     │       │   Celery    │
      │  User/History│      │  Cache/Tasks │       │   Workers   │
      └─────────────┘       └─────────────┘       └──────┬──────┘
                                                         │
                                                         ▼
                                                  ┌─────────────┐
                                                  │  LLM API    │
                                                  │  (Claude)   │
                                                  └─────────────┘
```

## Agent Responsibilities & Module Ownership

```
┌──────────────────────────────────────────────────────────┐
│                      Coordinator                          │
│                 任务拆解 & 进度跟踪                        │
└────────────────────────┬─────────────────────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
    ▼                    ▼                    ▼
┌─────────┐      ┌──────────────┐      ┌──────────┐
│architect│      │   backend    │      │ frontend │
│ 架构设计 │      │    -dev      │      │   -dev   │
│         │      │ API/DB/      │      │ React UI │
│ 整体架构 │      │ 集成/缓存    │      │ 可视化   │
└────┬────┘      └──────┬───────┘      └────┬─────┘
     │                  │                   │
     └──────────────────┼───────────────────┘
                        │
    ┌───────────────────┼───────────────────┐
    │                   │                   │
    ▼                   ▼                   ▼
┌──────────┐    ┌──────────────┐    ┌──────────────┐
│algorithm │    │      qa      │    │    devops    │
│engineer  │    │  -engineer   │    │  -engineer   │
│ NLP/评分 │    │ 测试/质量    │    │ CI/CD/部署   │
└──────────┘    └──────────────┘    └──────────────┘
```

## Decisions

### 1. Backend: FastAPI over Flask
- **选择**: FastAPI
- **理由**: 原生异步支持（async/await），自动生成OpenAPI文档，Pydantic数据验证，更好的类型提示支持。对于需要调用LLM API的IO密集型应用，异步性能优势明显。

### 2. LLM集成: Claude API (anthropic SDK)
- **选择**: Claude API via `anthropic` Python SDK
- **理由**: 中文理解能力强，支持系统提示词定制优化策略，结构化输出（JSON mode）便于解析优化建议。

### 3. 前端: React 18 + Ant Design
- **选择**: React + Ant Design
- **理由**: Ant Design提供成熟的表单、表格、图表组件，中文生态完善，适合数据密集型后台管理界面。

### 4. 标题评分模型: 规则引擎 + LLM 混合架构
- **选择**: 规则引擎处理基础维度（长度、emoji、标签数量），LLM处理高维度（吸引力、情绪触发、创意度）
- **理由**: 纯LLM成本高、延迟大；纯规则灵活性不足。混合架构兼顾成本和效果。

### 5. 任务队列: Celery + Redis
- **选择**: Celery with Redis broker
- **理由**: 批量优化场景需要异步处理，Celery生态成熟，Redis既做缓存又做消息队列，减少基础设施复杂度。

## Project Structure

```
tiktok-title-optimizer/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI route handlers
│   │   │   ├── v1/
│   │   │   │   ├── optimize.py
│   │   │   │   ├── history.py
│   │   │   │   └── auth.py
│   │   │   └── deps.py       # Dependency injection
│   │   ├── core/
│   │   │   ├── config.py     # Settings
│   │   │   └── security.py   # JWT, password hashing
│   │   ├── models/           # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   └── optimization.py
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   │   ├── optimizer/
│   │   │   └── scorer/
│   │   └── tasks/            # Celery tasks
│   ├── alembic/              # DB migrations
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # Shared components
│   │   ├── pages/            # Route pages
│   │   │   ├── Dashboard/
│   │   │   ├── Optimizer/
│   │   │   └── History/
│   │   ├── hooks/            # Custom hooks
│   │   ├── api/              # API client
│   │   └── stores/           # State management
│   └── package.json
├── algorithms/
│   ├── scoring/              # Scoring rules & models
│   ├── nlp/                  # Keyword extraction, analysis
│   ├── optimizer/            # LLM-based optimization
│   └── features/             # Feature extraction
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── Makefile
```

## Risks / Trade-offs

- **[LLM调用成本]** 每次优化调用Claude API产生费用 → 实现缓存层避免重复优化，规则引擎预处理减少不必要的LLM调用
- **[LLM响应延迟]** 远程API调用增加响应时间 → 异步处理+前端loading状态优化用户体验，Celery后台批量处理
- **[中文分词精度]** jieba分词在抖音网络热词上可能不准 → 维护自定义词典，结合LLM进行新词识别
- **[评分模型主观性]** 标题吸引力评估存在主观偏差 → 支持用户反馈机制（点赞/踩），逐步校准评分权重

## Open Questions

- 是否需要在V1版本就集成TikTok API获取真实播放量作为反馈信号？
- 用户免费额度策略（每日优化次数限制）？
- 是否需要支持多语言标题优化（如英文TikTok标题）？
