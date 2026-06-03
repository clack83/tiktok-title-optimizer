## Why

抖音内容创作者面临标题优化的核心痛点：缺乏数据驱动的优化工具，凭经验撰写的标题往往无法最大化播放量和互动率。本项目旨在打造一个基于AI的抖音标题优化器，帮助创作者通过智能分析和优化建议，快速生成高吸引力标题，提升内容传播效果。

## What Changes

- **新增** 标题优化核心引擎：集成NLP分析和LLM优化能力，支持多维度标题评分和自动优化建议生成
- **新增** Web应用界面：提供标题输入、优化结果展示、历史记录管理和数据看板
- **新增** 后端API服务：RESTful API 支持标题优化请求、用户管理、数据持久化
- **新增** 数据库层：PostgreSQL 存储用户数据、优化历史、标题特征；Redis 缓存热门分析结果
- **新增** 批量优化能力：支持通过Celery任务队列批量处理标题优化

## Capabilities

### New Capabilities
- `title-scoring`: 标题多维度质量评分系统（吸引力、信息量、可读性、平台适配）
- `title-optimization`: 基于LLM的标题优化建议生成器，支持多种优化策略
- `keyword-analysis`: 关键词提取与热门话题匹配分析
- `user-management`: 用户注册、登录、偏好设置管理
- `optimization-history`: 优化历史记录存储、查询和对比分析
- `data-dashboard`: 数据看板展示优化效果趋势、热门关键词云、评分分布

### Modified Capabilities
<!-- 首次创建，无需修改现有能力 -->

## Impact

- **代码**: 全新项目，从零搭建。涉及 frontend/、backend/、algorithms/ 三大核心模块
- **API**: 需要集成第三方LLM API (Claude API)，预留 TikTok API 集成接口
- **数据库**: PostgreSQL（主存储）、Redis（缓存/任务队列）
- **部署**: Docker Compose 多容器编排，GitHub Actions CI/CD
- **依赖**: FastAPI, SQLAlchemy, Celery, React 18, Ant Design, jieba, transformers
- **团队分工**: architect（架构设计）、backend-dev（API/数据库）、frontend-dev（UI/数据可视化）、algorithm-engineer（评分模型/NLP）、qa-engineer（测试）、devops-engineer（CI/CD/部署）
