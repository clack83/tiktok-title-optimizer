## 1. DeepSeek API 集成与配置 [algorithm-engineer + devops-engineer]

- [x] 1.1 移除 `anthropic` 依赖，添加 `openai` SDK 到 requirements.txt [algorithm-engineer]
- [x] 1.2 实现 DeepSeek 客户端封装类（base_url, api_key, model="deepseek-chat"）[algorithm-engineer]
- [x] 1.3 添加 DEEPSEEK_API_KEY 和 DEEPSEEK_BASE_URL 环境变量配置 [devops-engineer] [并行]
- [x] 1.4 实现指数退避重试机制（max 3 retries, base delay 1s）[algorithm-engineer]
- [x] 1.5 更新 docker-compose.yml 和 .env.example 文件 [devops-engineer] [并行]

## 2. 分类提示词系统 [algorithm-engineer]

- [x] 2.1 创建 `algorithms/categories.yaml` 配置文件，定义 10 个垂直分类 [algorithm-engineer]
- [x] 2.2 为每个分类编写爆款提示词（context_keywords, hook_patterns, audience, taboos）[algorithm-engineer]
- [x] 2.3 实现分类配置 YAML 加载器和热加载机制（60s 刷新）[algorithm-engineer]
- [x] 2.4 实现分类提示词注入到 system prompt 的逻辑 [algorithm-engineer]
- [x] 2.5 更新优化流水线：接收 category 参数 → 查询分类配置 → 注入 prompt → 调用 DeepSeek [algorithm-engineer]

## 3. 修改理由生成逻辑 [algorithm-engineer]

- [x] 3.1 设计并实现 change_reasons 的 prompt 模板（要求 LLM 返回结构化理由）[algorithm-engineer]
- [x] 3.2 更新优化 prompt：要求每条优化标题附带 category + comparison + reason + expected_effect [algorithm-engineer]
- [x] 3.3 实现 change_reasons 响应解析和校验（每条标题至少 3 条理由）[algorithm-engineer]
- [x] 3.4 更新 `OptimizationRecord` 模型和 Pydantic schema 增加 change_reasons 字段 [algorithm-engineer]

## 4. 评分解释增强 [algorithm-engineer]

- [x] 4.1 重构评分解释输出格式：从单句升级为 {diagnosis, improvement, expected_effect} 三段式 [algorithm-engineer]
- [x] 4.2 实现解释生成中的原文引用功能（诊断时引用标题具体词汇）[algorithm-engineer]
- [x] 4.3 更新 POST /api/v1/optimize/score 端点的 Pydantic response schema [algorithm-engineer]

## 5. 后端 API 变更 [backend-dev]

- [x] 5.1 新增 GET /api/v1/categories 端点，返回分类列表 [backend-dev]
- [x] 5.2 更新 POST /api/v1/optimize 端点：接收可选的 `category` 字段，校验分类有效性 [backend-dev]
- [x] 5.3 更新 POST /api/v1/optimize 响应 schema：增加 `change_reasons` 字段 [backend-dev] [并行]
- [x] 5.4 更新 POST /api/v1/optimize/score 响应 schema：三段式解释格式 [backend-dev] [并行]
- [x] 5.5 更新 POST /api/v1/optimize/batch 端点：支持共享 category 参数 [backend-dev]
- [x] 5.6 更新 Redis 缓存 key 策略：hash(title + strategy + category) 替代原有 hash(title + strategy) [backend-dev]

## 6. 前端 - 分类选择组件 [frontend-dev]

- [x] 6.1 在 Optimizer 页面添加分类下拉选择器（Ant Design Select）[frontend-dev]
- [x] 6.2 对接 GET /api/v1/categories API，渲染分类选项（含图标和名称）[frontend-dev]
- [x] 6.3 分类选择后，在输入框下方展示该分类的提示词标签供用户参考 [frontend-dev]

## 7. 前端 - 优化结果与修改理由展示 [frontend-dev]

- [x] 7.1 实现修改理由展开面板组件（每条优化标题卡片内可展开查看理由）[frontend-dev]
- [x] 7.2 实现改前/改后对比高亮组件（comparison.before vs comparison.after 差异展示）[frontend-dev]
- [x] 7.3 实现优化理由分类标签（hook_enhancement → "钩子增强" 等中文映射）[frontend-dev] [并行]
- [x] 7.4 实现评分诊断卡片组件（默认折叠显示分数，点击展开显示 diagnosis/improvement/expected_effect）[frontend-dev]
- [x] 7.5 优化理由区添加可折叠/展开全部功能 [frontend-dev] [并行]

## 8. 前端 - 批量优化支持分类 [frontend-dev]

- [x] 8.1 批量优化页面添加分类选择器（批量模式共享分类）[frontend-dev]
- [x] 8.2 批量结果列表适配 change_reasons 展示（每条标题支持展开查看理由）[frontend-dev]

## 9. 测试与验证 [qa-engineer]

- [x] 9.1 编写 DeepSeek 客户端单元测试（mock API 响应，验证重试逻辑）[qa-engineer]
- [x] 9.2 编写分类加载和热更新测试（模拟 YAML 文件变更）[qa-engineer] [并行]
- [x] 9.3 编写 change_reasons 解析测试（验证至少 3 条理由，格式完整性）[qa-engineer] [并行]
- [x] 9.4 编写评分解释三段式格式测试 [qa-engineer] [并行]
- [x] 9.5 编写 API 端点测试（categories, optimize with category, score explanations）[qa-engineer]
- [x] 9.6 编写前端组件测试（分类选择器、理由展开面板、诊断卡片）[qa-engineer] [并行]
- [x] 9.7 E2E 测试：选择分类 → 输入标题 → 查看优化结果 → 展开修改理由 → 验证评分诊断 [qa-engineer]
