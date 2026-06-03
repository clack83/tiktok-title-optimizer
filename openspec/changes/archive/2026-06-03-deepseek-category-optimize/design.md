## Context

基于 `init-title-optimizer` 已有架构设计，本次变更聚焦三个核心修改：LLM 供应商从 Claude 切换到 DeepSeek、增加垂直领域分类提示词系统、优化结果增加结构化修改理由。架构层面不做大改动，主要调整算法模块和前端交互。

## Goals / Non-Goals

**Goals:**
- DeepSeek API 完整替代 Claude API，保持原有优化能力不变
- 预设至少 10 个垂直领域分类，每个分类包含该领域的爆款提示词模板
- 每条优化标题附带至少 3 条结构化修改理由（改了哪里、为什么改、预期效果）
- 评分解释从一句话升级为"问题诊断 + 改进方向 + 预期效果"三段式

**Non-Goals:**
- 不改变整体架构（FastAPI + React + PostgreSQL + Redis + Celery 保持不变）
- 不支持用户自定义分类（V1 使用预设分类）
- 不做 DeepSeek vs Claude 对比评估功能

## Decisions

### 1. DeepSeek API 接入方式: OpenAI 兼容 SDK
- **选择**: 使用 `openai` Python SDK，配置 `base_url="https://api.deepseek.com"`
- **理由**: DeepSeek API 与 OpenAI API 格式兼容，`openai` SDK 生态成熟、文档丰富。切换成本极低，只需修改 `base_url` 和 `api_key`。
- **备选方案**: 直接 HTTP 请求（dropped: 缺少流式支持和重试机制）
- **模型**: `deepseek-chat`（性价比最优，中文能力与 deepseek-reasoner 在标题生成场景差异不大）

### 2. 分类提示词系统: YAML 配置文件 + Jinja2 模板注入
- **选择**: 分类数据存储在 `algorithms/categories.yaml`，使用 Jinja2 将分类提示词注入 system prompt 模板
- **理由**: YAML 配置文件便于维护和扩展分类，非技术人员也能修改；Jinja2 模板灵活地将分类知识注入 prompt

```
categories.yaml 结构:
categories:
  gaming:           # 游戏
    name: "游戏"
    icon: "gamepad"
    context_keywords: ["攻略", "操作", "通关", "上分", "新皮肤"]
    hook_patterns:
      - "学会这招直接{action}"
      - "90%的玩家不知道{secret}"
    audience: "18-30岁男性为主，追求技术和娱乐"
    taboos: ["虚假宣传", "外挂相关"]
  lifestyle:        # 生活
    ...
```

### 3. 修改理由结构: 三层理由模型
- **选择**: 每条修改理由包含 `category`（改动类型）, `comparison`（改前/改后对比）, `reason`（为什么改）, `expected_effect`（预期效果）
- **理由**: 单纯给一句说明不够有说服力。三层结构让用户看清"改了什么 → 为什么 → 有什么好处"，建立信任感。

```
change_reasons 输出格式:
[
  {
    "category": "hook_enhancement",
    "comparison": {"before": "分享护肤小知识", "after": "我用了这个方法，皮肤直接逆袭"},
    "reason": "原标题缺乏hook，读者没有点击欲望。用第一人称+结果转折制造悬念",
    "expected_effect": "提升点击率约20-30%，增加停留时长"
  },
  ...
]
```

### 4. 评分解释增强: 诊断式反馈
- **选择**: 评分解释从单句升级为 `{diagnosis, improvement, expected_effect}` 三段式
- **理由**: 原有解释只说"吸引力不足"，用户不知道怎样改。诊断式反馈给出具体问题和可行方向。

## Risks / Trade-offs

- **[DeepSeek API 稳定性]** DeepSeek 作为国产服务可能有高峰期限流 → 实现指数退避重试（max 3次），降级到规则引擎兜底
- **[分类提示词维护成本]** 10个分类的爆款提示词可能过时 → 设计 YAML 热加载，无需重启服务即可更新；预留 LLM 自动更新提示词的扩展点
- **[修改理由质量依赖 LLM]** 理由由 LLM 生成，可能不够准确 → prompt 中严格要求理由粒度（每条理由必须引用原标题的具体位置），前端用格式标记（对比高亮）让用户一目了然
- **[响应体积增大]** 增加 change_reasons 和诊断式解释后，响应体增大 40-60% → 批量优化时支持按需返回（?include_reasons=true/false）

## Migration Plan

1. 新增 `deepseek` 配置项，保留原有 Claude 配置但不启用（切换开关）
2. 新增 `categories.yaml` 配置文件，数据不影响已有功能
3. 新增 API 字段 `category`（optional，不传则全领域优化）和 `change_reasons`（始终返回，前端按需展示）
4. 数据库 JSON 字段自动兼容新增的 `change_reasons` 结构（无需 migration）
5. 前端新增分类下拉组件和理由展开面板（纯增量，不破坏已有 UI）
