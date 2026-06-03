## MODIFIED Requirements

### Requirement: Single title optimization
The system SHALL accept a single title string with an optional category selection and return 3-5 optimized variations, each with structured change reasons explaining what was changed, why, and the expected effect.

#### Scenario: Optimize a weak title
- **WHEN** user submits title "分享一个护肤小知识"
- **THEN** system returns 3-5 optimized variations, each with a score delta showing improvement over original, and a `change_reasons` array with at least 3 entries explaining specific modifications

#### Scenario: Optimize with category context
- **WHEN** user submits title "教程" with category "美妆" and topic keywords "新手化妆"
- **THEN** optimization SHALL incorporate both category-specific viral patterns and the user-provided topic keywords into generated titles

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

### Requirement: Multi-strategy optimization
The system SHALL support at least 4 optimization strategies: hook enhancement, emotional amplification, keyword optimization, and formatting polish. Strategy selection SHALL be influenced by the selected category's characteristics.

#### Scenario: Auto strategy by category
- **WHEN** user selects category "科技" without specifying a strategy
- **THEN** system SHALL prefer "keyword_optimization" and "formatting_polish" strategies (tech audience prefers information-dense, well-structured titles)

#### Scenario: Gaming category favors hook enhancement
- **WHEN** user selects category "游戏" without specifying a strategy
- **THEN** system SHALL prefer "hook_enhancement" and "emotional_amplification" strategies (gaming audience responds to challenge and excitement hooks)

### Requirement: Optimization result caching
The system SHALL cache optimization results in Redis with a 24-hour TTL, keyed by hash of (title + strategy + category) to avoid redundant LLM calls for identical requests.

#### Scenario: Same title, different category
- **WHEN** the same title is submitted with different category selections
- **THEN** system SHALL NOT return cached results from a different category, and SHALL perform a new optimization

### Requirement: Batch optimization
The system SHALL support batch optimization via Celery task queue, allowing users to submit up to 50 titles at once with an optional shared category.

#### Scenario: Batch with shared category
- **WHEN** user submits 20 titles with category "美食"
- **THEN** all 20 titles SHALL be optimized using food-category prompt injection

#### Scenario: Batch status includes change reasons
- **WHEN** user queries completed batch task status
- **THEN** each optimized title in the result SHALL include full `change_reasons` arrays

## ADDED Requirements

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

