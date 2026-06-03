## 1. 数据库模型与配置 [backend-dev + architect]

- [x] 1.1 创建 `seed_titles` 表 SQLAlchemy 模型（id, category, title, score, hook_type, generated_at, is_active）[backend-dev]
- [ ] 1.2 创建 `seed_titles` 表 Alembic migration 脚本 [backend-dev]
- [x] 1.3 编写 seed_titles 的 Pydantic schema（请求/响应）[backend-dev] [并行]

## 2. 种子标题生成引擎 [algorithm-engineer]

- [x] 2.1 实现种子生成 prompt 模板（要求 DeepSeek 生成指定分类的爆款标题，含多样性约束）[algorithm-engineer]
- [x] 2.2 实现种子标题批量生成服务：调用 DeepSeek → 提取标题 → 调用评分引擎打分 → 过滤 >=70 [algorithm-engineer]
- [x] 2.3 实现去重逻辑（jieba token overlap > 80% 则保留高分者）[algorithm-engineer]
- [x] 2.4 实现 hook 类型多样性检查（确保至少覆盖 4 种不同 hook_type）[algorithm-engineer]
- [x] 2.5 实现质量不足时的补充生成逻辑（最多额外 2 轮）[algorithm-engineer] [并行]

## 3. 种子库 API [backend-dev]

- [x] 3.1 实现 GET /api/v1/seeds?category=XX 查询端点 [backend-dev]
- [x] 3.2 实现 GET /api/v1/seeds 无分类汇总查询（按分类分组，每类 top 5）[backend-dev] [并行]
- [x] 3.3 实现 POST /api/v1/seeds/refresh 刷新端点（支持单分类和全刷新）[backend-dev]
- [x] 3.4 实现种子标题 Redis 缓存层（5 分钟 TTL，按分类 key）[backend-dev]
- [x] 3.5 更新 GET /api/v1/categories 端点增加 seed_count 和 seed_preview 字段 [backend-dev]

## 4. 优化 Prompt 增强 [algorithm-engineer]

- [x] 4.1 实现 few-shot 种子筛选算法（基于用户输入关键词与种子标题的 jieba token 重叠度）[algorithm-engineer]
- [x] 4.2 更新优化 prompt 模板：新增"参考爆款标题"动态段 [algorithm-engineer]
- [x] 4.3 实现种子不可用时的降级策略（无参考 → 正常优化 + warnings 标记）[algorithm-engineer]
- [x] 4.4 更新 POST /api/v1/optimize 响应增加 seeds_used 字段（记录实际使用的种子 ID）[algorithm-engineer]

## 5. Celery 后台任务 [backend-dev + algorithm-engineer]

- [x] 5.1 实现 `generate_seeds` Celery 任务（接收 category 参数，调用生成引擎）[algorithm-engineer]
- [x] 5.2 实现 `refresh_all_seeds` Celery 协调任务（并行触发 10 个分类生成任务）[algorithm-engineer] [并行]
- [x] 5.3 配置 Celery Beat 定时任务：每周日凌晨 3 点执行 refresh_all_seeds [devops-engineer]

## 6. 前端 - 种子标题展示 [frontend-dev]

- [x] 6.1 在 Optimizer 页面增加"爆款参考"侧边栏/Tab [frontend-dev]
- [x] 6.2 实现种子标题列表组件（按评分排序，显示分数和 hook 类型标签）[frontend-dev]
- [x] 6.3 实现分类切换时种子列表联动刷新 [frontend-dev] [并行]
- [x] 6.4 实现分类下拉的选择项增强（显示 seed_count + hover 时 top 3 预览）[frontend-dev]
- [x] 6.5 实现空状态展示（种子生成中... 提示）[frontend-dev] [并行]

## 7. 测试 [qa-engineer]

- [x] 7.1 编写种子生成引擎单元测试（mock DeepSeek，验证过滤和去重逻辑）[qa-engineer]
- [x] 7.2 编写 GET /api/v1/seeds 端点测试（按分类、无分类、空分类）[qa-engineer] [并行]
- [x] 7.3 编写 POST /api/v1/seeds/refresh 端点测试（单分类、全刷新）[qa-engineer] [并行]
- [x] 7.4 编写 few-shot 筛选算法测试（验证关键词重叠度计算和 top-N 选择）[qa-engineer]
- [x] 7.5 编写优化 prompt 增强测试（验证 seeds 正确注入 prompt，降级逻辑正常）[qa-engineer] [并行]
- [x] 7.6 编写种子多样性测试（验证 hook 类型覆盖，去重效果）[qa-engineer] [并行]
- [ ] 7.7 编写前端组件测试（种子列表、分类预览、空状态）[qa-engineer]
