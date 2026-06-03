## 1. 项目基础设施搭建

- [x] 1.1 创建项目目录结构和 Python 虚拟环境 [architect + devops-engineer] [并行]
- [x] 1.2 编写 backend/requirements.txt（FastAPI, SQLAlchemy, Celery, jieba, openai 等）[devops-engineer]
- [x] 1.3 编写 frontend/package.json（React 18, TypeScript, Ant Design, ECharts）[devops-engineer] [并行]
- [x] 1.4 编写 Dockerfile.backend 和 Dockerfile.frontend [devops-engineer] [并行]
- [x] 1.5 编写 docker-compose.yml（backend, frontend, postgres, redis, celery_worker）[devops-engineer]
- [x] 1.6 配置 GitHub Actions CI/CD 流水线（lint → test → build）[devops-engineer]
- [x] 1.7 编写 Makefile（常用命令：dev, test, lint, build, migrate）[devops-engineer] [并行]

## 2. 数据库模型与迁移

- [x] 2.1 设计并实现 User SQLAlchemy 模型（id, email, password_hash, created_at）[backend-dev]
- [x] 2.2 设计并实现 OptimizationRecord SQLAlchemy 模型（id, user_id, original_title, results JSON, scores JSON, strategy, created_at）[backend-dev]
- [x] 2.3 设计并实现 UserPreference SQLAlchemy 模型（id, user_id, preferences JSON）[backend-dev] [并行]
- [x] 2.4 配置 Alembic 数据库迁移环境，生成初始 migration [backend-dev]
- [x] 2.5 编写 Redis 连接和缓存工具类 [backend-dev] [并行]

## 3. 用户认证与偏好管理

- [x] 3.1 实现用户注册端点 POST /api/v1/auth/register [backend-dev]
- [x] 3.2 实现用户登录端点 POST /api/v1/auth/login（JWT access + refresh token）[backend-dev]
- [x] 3.3 实现 Token 刷新端点 POST /api/v1/auth/refresh [backend-dev] [并行]
- [x] 3.4 实现 JWT 认证中间件和依赖注入（get_current_user）[backend-dev]
- [x] 3.5 实现用户偏好 CRUD 端点 GET/PUT /api/v1/user/preferences [backend-dev]

## 4. 标题评分引擎

- [x] 4.1 实现评分规则引擎基础框架（register/evaluate 模式）[algorithm-engineer]
- [x] 4.2 实现吸引力维度评分规则（hook强度、情绪触发、权力词检测）[algorithm-engineer] [并行]
- [x] 4.3 实现信息量维度评分规则（数字、具体承诺、关键词密度）[algorithm-engineer] [并行]
- [x] 4.4 实现可读性维度评分规则（长度、分词、歧义检测）[algorithm-engineer] [并行]
- [x] 4.5 实现平台适配维度评分规则（emoji使用、标签策略）[algorithm-engineer] [并行]
- [x] 4.6 实现评分解释生成器（每个维度输出中文解释）[algorithm-engineer]

## 5. 关键词分析与话题匹配

- [x] 5.1 配置 jieba 分词并维护抖音热词自定义词典 [algorithm-engineer]
- [x] 5.2 实现关键词提取服务（jieba 分词 + TF-IDF 权重计算）[algorithm-engineer]
- [x] 5.3 创建热门话题词库 seed data 和维护接口 [algorithm-engineer] [并行]
- [x] 5.4 实现关键词与热门话题匹配算法 [algorithm-engineer]

## 6. 标题优化引擎

- [x] 6.1 封装 DeepSeek API 客户端（openai SDK，结构化 prompt 模板，指数退避重试）[algorithm-engineer]
- [x] 6.2 实现 4 种优化策略的 prompt 模板（hook增强、情绪放大、关键词优化、格式润色）[algorithm-engineer]
- [x] 6.3 实现混合优化流水线（规则引擎初步评分 → LLM 优化 → 二次评分对比）[algorithm-engineer]
- [x] 6.4 实现优化结果 Redis 缓存层（24h TTL，基于 title+strategy hash key）[algorithm-engineer]

## 7. 后端 API - 核心优化端点

- [x] 7.1 实现 POST /api/v1/optimize - 单条标题优化端点 [backend-dev]
- [x] 7.2 实现 POST /api/v1/optimize/score - 标题评分端点 [backend-dev] [并行]
- [x] 7.3 实现 POST /api/v1/optimize/keywords - 关键词提取端点 [backend-dev] [并行]
- [x] 7.4 实现 POST /api/v1/optimize/batch - 批量优化端点（返回 celery task_id）[backend-dev]
- [x] 7.5 实现 GET /api/v1/optimize/batch/{task_id} - 批量任务状态查询端点 [backend-dev]

## 8. 后端 API - 历史记录与数据看板

- [x] 8.1 实现 GET /api/v1/history - 优化历史分页查询端点 [backend-dev]
- [x] 8.2 实现 DELETE /api/v1/history/{id} - 删除历史记录端点 [backend-dev] [并行]
- [x] 8.3 实现 POST /api/v1/history/compare - 两条记录对比端点 [backend-dev] [并行]
- [x] 8.4 实现 GET /api/v1/dashboard/overview - 数据看板概览统计 [backend-dev]
- [x] 8.5 实现 GET /api/v1/dashboard/trends - 评分趋势数据 [backend-dev] [并行]
- [x] 8.6 实现 GET /api/v1/dashboard/keywords-cloud - 关键词云数据 [backend-dev] [并行]
- [x] 8.7 实现 GET /api/v1/dashboard/score-distribution - 评分分布数据 [backend-dev] [并行]

## 9. Celery 异步任务

- [x] 9.1 配置 Celery app（Redis broker, result backend）[backend-dev]
- [x] 9.2 实现 batch_optimize Celery 任务（遍历标题列表，调用优化引擎）[backend-dev]
- [x] 9.3 实现任务进度回调与结果存储 [backend-dev] [并行]

## 10. 前端项目搭建与认证模块

- [x] 10.1 创建 React + TypeScript 项目脚手架（Vite 构建）[frontend-dev]
- [x] 10.2 配置 Ant Design、React Router、API 客户端（axios）[frontend-dev]
- [x] 10.3 实现注册页面组件（邮箱、密码、确认密码表单）[frontend-dev] [并行]
- [x] 10.4 实现登录页面组件（邮箱、密码、记住我）[frontend-dev] [并行]
- [x] 10.5 实现认证状态管理（JWT 存储、自动刷新、路由守卫）[frontend-dev]

## 11. 前端 - 标题优化界面

- [x] 11.1 实现标题输入组件（单条+批量 Tab 切换、内容分类选择、策略选择）[frontend-dev]
- [x] 11.2 实现优化结果展示组件（原始标题 vs 优化标题对比卡片、评分变化、优化建议说明）[frontend-dev]
- [x] 11.3 实现批量优化进度展示组件（进度条、完成数/总数）[frontend-dev] [并行]
- [x] 11.4 实现关键词分析结果展示（关键词标签、热门话题匹配）[frontend-dev]

## 12. 前端 - 历史记录与数据看板

- [x] 12.1 实现优化历史列表页（表格、日期筛选、分页）[frontend-dev]
- [x] 12.2 实现历史记录对比视图（左右分栏对比）[frontend-dev] [并行]
- [x] 12.3 实现数据看板概览卡片（总优化次数、平均提升、常用策略）[frontend-dev]
- [x] 12.4 实现评分趋势折线图（ECharts）[frontend-dev] [并行]
- [x] 12.5 实现关键词云图（ECharts wordCloud）[frontend-dev] [并行]
- [x] 12.6 实现评分分布柱状图（ECharts）[frontend-dev] [并行]

## 13. 测试

- [x] 13.1 编写评分引擎单元测试（各维度评分规则覆盖率 >90%）[qa-engineer]
- [x] 13.2 编写优化引擎单元测试（mock LLM 响应，测试策略选择逻辑）[qa-engineer] [并行]
- [x] 13.3 编写关键词提取单元测试（分词精度测试、自定词典验证）[qa-engineer] [并行]
- [x] 13.4 编写 API 端点集成测试（auth, optimize, history, dashboard）[qa-engineer]
- [x] 13.5 编写前端组件测试（输入组件、结果展示、历史列表）[qa-engineer] [并行]
- [x] 13.6 编写 E2E 测试用例（注册→登录→优化标题→查看历史→看板全流程）[qa-engineer]
- [x] 13.7 编写性能基准测试（API 响应时间 < 200ms, 批量50条 < 5min）[qa-engineer] [并行]

## 14. 最终集成与验证

- [x] 14.1 Docker Compose 全栈启动验证 [devops-engineer]
- [x] 14.2 端到端功能验收（按 spec 场景逐一验证）[all agents]
- [x] 14.3 CI/CD 流水线全量通过验证 [devops-engineer]
