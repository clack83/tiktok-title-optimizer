# title-optimization Specification

## Purpose
TBD - created by archiving change viral-title-seed-library. Update Purpose after archive.
## Requirements
### Requirement: Few-shot seed injection in optimization prompt
The system SHALL inject 3-5 relevant seed titles from the selected category into the system prompt as few-shot style examples during optimization.

#### Scenario: Prompt includes seed examples
- **WHEN** user optimizes a title with category "旅行"
- **THEN** the system prompt sent to DeepSeek SHALL include a "参考爆款标题" section listing 3-5 seed titles from the travel category with their scores

#### Scenario: Seeds not available for category
- **WHEN** user optimizes with a category that has no generated seeds yet
- **THEN** optimization SHALL proceed normally without few-shot examples, and the response SHALL include a warning flag "seeds_unavailable: true"

#### Scenario: Seeds improve output quality
- **WHEN** optimization includes seed examples vs not including them
- **THEN** the generated titles SHALL better match the category's viral patterns (verified via LLM-as-judge evaluation in test suite)

### Requirement: Optimization prompt template update
The system prompt template SHALL be updated to include a dynamic "参考风格" section that renders category-specific seed titles when available.

#### Scenario: Prompt template renders seeds
- **WHEN** building the optimization prompt for category "游戏"
- **THEN** the final prompt SHALL contain a section formatted as:
  ```
  ## 参考爆款标题（同领域高质量示例）
  1. "学了三年的打野套路，今天全教给你" [评分: 89]
  2. "王者新赛季这些英雄直接起飞" [评分: 85]
  3. "90%的玩家都不知道的卡视野技巧" [评分: 82]

  请在以上风格基础上，优化用户标题。
  ```

### Requirement: Single title optimization
The system SHALL accept a single title string with an optional category selection and return 3-5 optimized variations, each with structured change reasons explaining what was changed, why, and the expected effect.

#### Scenario: Optimize a weak title
- **WHEN** user submits title "分享一个护肤小知识"
- **THEN** system returns 3-5 optimized variations, each with a score delta showing improvement over original, and a `change_reasons` array with at least 3 entries explaining specific modifications

#### Scenario: Optimize with category context
- **WHEN** user submits title "教程" with category "美妆" and topic keywords "新手化妆"
- **THEN** optimization SHALL incorporate both category-specific viral patterns and the user-provided topic keywords into generated titles

### Requirement: Multi-strategy optimization
The system SHALL support at least 4 optimization strategies: hook enhancement, emotional amplification, keyword optimization, and formatting polish. Strategy selection SHALL be influenced by the selected category's characteristics.

#### Scenario: Auto strategy by category
- **WHEN** user selects category "科技" without specifying a strategy
- **THEN** system SHALL prefer "keyword_optimization" and "formatting_polish" strategies (tech audience prefers information-dense, well-structured titles)

#### Scenario: Gaming category favors hook enhancement
- **WHEN** user selects category "游戏" without specifying a strategy
- **THEN** system SHALL prefer "hook_enhancement" and "emotional_amplification" strategies (gaming audience responds to challenge and excitement hooks)

### Requirement: LLM-based generation
The system SHALL use DeepSeek API (`openai` SDK with `deepseek-chat` model) to generate optimized title variations with structured prompts that enforce TikTok best practices and category-specific patterns.

#### Scenario: DeepSeek returns structured response
- **WHEN** calling DeepSeek API for optimization
- **THEN** the prompt SHALL request JSON-formatted output with fields: title, score_estimate, change_reasons (array of {category, comparison, reason, expected_effect})

#### Scenario: DeepSeek call fails
- **WHEN** DeepSeek API returns an error or times out after 30 seconds
- **THEN** system SHALL retry with exponential backoff (max 3 retries), then return HTTP 502 with message "优化服务暂时不可用，请稍后重试" and log the error

#### Scenario: DeepSeek retry success
- **WHEN** DeepSeek API first call fails but retry succeeds within 3 attempts
- **THEN** system SHALL return the optimization result normally and log a warning about the retry

### Requirement: Batch optimization
The system SHALL support batch optimization via Celery task queue, allowing users to submit up to 50 titles at once with an optional shared category.

#### Scenario: Batch with shared category
- **WHEN** user submits 20 titles with category "美食"
- **THEN** all 20 titles SHALL be optimized using food-category prompt injection

#### Scenario: Batch status includes change reasons
- **WHEN** user queries completed batch task status
- **THEN** each optimized title in the result SHALL include full `change_reasons` arrays

### Requirement: Optimization result caching
The system SHALL cache optimization results in Redis with a 24-hour TTL, keyed by hash of (title + strategy + category) to avoid redundant LLM calls for identical requests.

#### Scenario: Same title, different category
- **WHEN** the same title is submitted with different category selections
- **THEN** system SHALL NOT return cached results from a different category, and SHALL perform a new optimization

### Requirement: Change reasons in optimization results
The system SHALL include structured modification reasons for each optimized title variant, using the format {category, comparison, reason, expected_effect}.

#### Scenario: Get detailed change reasons
- **WHEN** a title optimization returns 3 variations
- **THEN** each variation SHALL contain a `change_reasons` array with entries covering at least: hook modification, keyword changes, and formatting adjustments

#### Scenario: Change reason with comparison
- **WHEN** "试试这个简单方法" is optimized to "后悔没早知道的3个神技巧"
- **THEN** the change_reasons SHALL include an entry showing: {"category": "hook_enhancement", "comparison": {"before": "试试这个简单方法", "after": "后悔没早知道的3个神技巧"}, "reason": "原标题缺乏紧迫感和价值感，改用后悔体+数量钩子制造认知缺口", "expected_effect": "提升点击率约25%，增加好奇心驱动的完播"}

### Requirement: Category field in optimize request
The POST /api/v1/optimize endpoint SHALL accept an optional `category` field. When provided, optimization SHALL use the corresponding category's prompt configuration.

#### Scenario: Optimize with valid category
- **WHEN** user submits {"title": "今天学了一个新菜", "category": "美食"}
- **THEN** optimization SHALL use food-category viral patterns and audience preferences

#### Scenario: Optimize with invalid category
- **WHEN** user submits {"title": "...", "category": "invalid_category"}
- **THEN** system returns HTTP 422 with message "不支持该分类" and lists valid categories

