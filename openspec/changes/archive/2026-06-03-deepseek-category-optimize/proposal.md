## Why

原方案采用 Claude API 存在两个问题：1) 国内用户访问延迟高、成本不可控；2) 通用优化策略缺乏垂直领域针对性，无法生成符合行业爆款特征的标题。DeepSeek API 中文理解能力更强、国内访问延迟低、性价比更高。同时增加分类提示词系统和修改理由说明，可大幅提升优化效果的行业匹配度和用户信任度。

## What Changes

- **修改** LLM 供应商从 Claude API 切换到 DeepSeek API（`openai` 兼容 SDK），**BREAKING**: 原有 `anthropic` SDK 依赖废弃
- **新增** 内容分类下拉菜单（游戏、生活、旅行、婚恋、美食、科技、职场等），每个分类绑定垂直领域爆款提示词
- **新增** 优化结果必须包含每条修改建议的详细理由说明（为什么这样改、改了有什么效果）
- **修改** 评分解释从简短说明升级为结构化理由（问题诊断 + 改进方向 + 预期效果）

## Capabilities

### New Capabilities
- `category-prompts`: 垂直领域分类管理和行业爆款提示词引擎，每个分类预设爆款标题特征词、受众偏好、常见hook模式

### Modified Capabilities
- `title-optimization`: LLM API 从 Claude 切换为 DeepSeek；优化结果增加 `change_reasons` 字段，每条优化标题附带结构化修改理由
- `title-scoring`: 评分解释增强，输出从单句说明改为结构化诊断（问题 → 改进方向 → 预期效果）

## Impact

- **依赖**: 移除 `anthropic`，新增 `openai`（DeepSeek 兼容 OpenAI SDK 格式）
- **配置**: 新增 `DEEPSEEK_API_KEY`、`DEEPSEEK_BASE_URL` 环境变量；新增分类配置文件 `categories.yaml`
- **API**: `/api/v1/optimize` 请求体新增 `category` 字段；响应新增 `change_reasons` 数组
- **前端**: Optimizer 页面新增分类下拉组件；结果卡片新增修改理由展开面板
- **数据库**: OptimizationRecord 的 results JSON 扩展 `change_reasons` 字段
- **算法**: 优化引擎 prompt 模板增加分类提示词注入；增加修改理由生成逻辑
