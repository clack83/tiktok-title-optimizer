## Why

标题优化不能凭空创造——优质优化建议需要参考真实有效的爆款标题作为参照。但由于个人开发者无法接入抖音官方 API 获取真实高播放量数据，一个替代方案是：由 DeepSeek 模型根据各垂直领域的爆款特征，自动生成高质量参考标题库。这些种子标题可在用户优化时作为 few-shot 示例注入 prompt，显著提升优化质量，同时为用户提供直观的"这个行业的爆款长什么样"参考答案。

## What Changes

- **新增** 爆款标题种子库：按分类存储高质量参考标题，由 DeepSeek 自动批量生成
- **新增** 种子库浏览功能：用户选择分类后可查看该领域的爆款参考标题列表
- **修改** 优化 prompt 增强：优化时将筛选后的种子标题作为 few-shot 示例注入 system prompt
- **新增** 种子库刷新机制：支持通过后台任务定期重新生成种子标题（例如每周刷新），保持时效性

## Capabilities

### New Capabilities
- `seed-title-library`: 爆款标题种子库——按分类存储、浏览、生成、刷新的参考标题系统

### Modified Capabilities
- `title-optimization`: 优化 prompt 模板增加种子标题 few-shot 注入逻辑，使用种子标题作为风格参考
- `category-prompts`: 每个分类关联种子标题列表，分类详情 API 增加种子标题预览

## Impact

- **数据库**: 新增 `seed_titles` 表（id, category, title, score, generated_at, is_active）
- **API**: 新增 GET /api/v1/seeds?category=XX 种子查询端点；新增 POST /api/v1/seeds/refresh 触发刷新
- **前端**: Optimizer 页面新增"参考标题"侧边栏/Tab，展示当前分类下的爆款种子标题
- **算法**: 优化引擎 prompt 构建时注入 3-5 条同分类高评种子标题作为 few-shot
- **任务**: 新增 seed_generator Celery 任务，调用 DeepSeek 批量生成种子标题
