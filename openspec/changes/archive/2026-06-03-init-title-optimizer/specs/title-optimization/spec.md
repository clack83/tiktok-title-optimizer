## ADDED Requirements

### Requirement: Single title optimization
The system SHALL accept a single title string and return 3-5 optimized variations with improvement explanations.

#### Scenario: Optimize a weak title
- **WHEN** user submits title "分享一个护肤小知识"
- **THEN** system returns 3-5 optimized variations, each with a score delta showing improvement over original, and a brief explanation of what was changed

#### Scenario: Optimize with content context
- **WHEN** user submits title "教程" with context "美妆教程, 新手化妆"
- **THEN** optimization SHALL incorporate the context keywords into generated titles

### Requirement: Multi-strategy optimization
The system SHALL support at least 4 optimization strategies: hook enhancement, emotional amplification, keyword optimization, and formatting polish.

#### Scenario: Apply specific strategy
- **WHEN** user selects "hook_enhancement" strategy
- **THEN** all returned variations SHALL focus on stronger opening hooks while preserving original topic

#### Scenario: Auto strategy mode
- **WHEN** user does not specify a strategy
- **THEN** system SHALL automatically select the most impactful strategy based on initial scoring results

### Requirement: LLM-based generation
The system SHALL use Claude API to generate optimized title variations with structured prompts that enforce TikTok best practices.

#### Scenario: LLM returns structured response
- **WHEN** calling Claude API for optimization
- **THEN** the prompt SHALL request JSON-formatted output with fields: title, score_estimate, changes_summary

#### Scenario: LLM call fails
- **WHEN** Claude API returns an error or times out after 30 seconds
- **THEN** system SHALL return HTTP 502 with message "优化服务暂时不可用，请稍后重试" and log the error

### Requirement: Batch optimization
The system SHALL support batch optimization via Celery task queue, allowing users to submit up to 50 titles at once.

#### Scenario: Submit batch optimization
- **WHEN** user submits 20 titles for batch optimization
- **THEN** system returns a task_id immediately, and optimization SHALL proceed asynchronously via Celery workers

#### Scenario: Check batch status
- **WHEN** user queries status with task_id
- **THEN** system returns status (pending/processing/completed/failed) and results if completed

### Requirement: Optimization result caching
The system SHALL cache optimization results in Redis with a 24-hour TTL to avoid redundant LLM calls for identical titles.

#### Scenario: Duplicate title within 24 hours
- **WHEN** user submits a title already optimized within 24 hours
- **THEN** system SHALL return cached results instead of calling LLM again
