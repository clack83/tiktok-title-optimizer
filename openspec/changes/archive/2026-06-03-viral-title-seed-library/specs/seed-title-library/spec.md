## ADDED Requirements

### Requirement: Seed title generation per category
The system SHALL generate 15-20 high-quality seed titles for each content category using DeepSeek API, filtered by the scoring engine to only retain titles scoring >= 70.

#### Scenario: Generate seeds for gaming category
- **WHEN** system triggers seed generation for category "游戏"
- **THEN** DeepSeek generates 25 candidate titles, scoring engine evaluates each, and the top 15-20 titles scoring >= 70 are saved to the database with category="游戏"

#### Scenario: Insufficient quality candidates
- **WHEN** fewer than 15 candidates score >= 70
- **THEN** system SHALL request additional candidates from DeepSeek (up to 2 extra rounds) until 15 qualified seeds are obtained or max retries exhausted

### Requirement: Seed title query
The system SHALL provide an API to query seed titles by category, returning active seeds sorted by score descending.

#### Scenario: Query seeds for a category
- **WHEN** user requests GET /api/v1/seeds?category=美食
- **THEN** system returns up to 20 seed titles for the food category, each with fields: id, title, score, hook_type, generated_at

#### Scenario: Query without category filter
- **WHEN** user requests GET /api/v1/seeds without category parameter
- **THEN** system returns seeds grouped by category, with top 5 per category

#### Scenario: Category has no seeds yet
- **WHEN** user requests seeds for a category that has no generated seeds
- **THEN** system returns empty array with a hint message "该分类种子标题正在生成中，请稍后查看"

### Requirement: Seed title refresh
The system SHALL support manual and scheduled refresh of seed titles, deactivating old seeds and generating new ones.

#### Scenario: Manual refresh
- **WHEN** admin calls POST /api/v1/seeds/refresh with body {"category": "科技"}
- **THEN** system deactivates all existing seeds for "科技", generates new seeds, and returns the count of newly generated seeds

#### Scenario: Scheduled weekly refresh
- **WHEN** Celery Beat triggers the weekly seed refresh task
- **THEN** all 10 categories SHALL be refreshed sequentially, and a summary report (success/fail per category) SHALL be logged

#### Scenario: Refresh all categories
- **WHEN** POST /api/v1/seeds/refresh is called without category
- **THEN** all 10 categories SHALL be refreshed in parallel using Celery tasks

### Requirement: Seed title diversity
The system SHALL ensure generated seed titles include diverse hook types within each category, avoiding stylistic repetition.

#### Scenario: Diverse hook types in category
- **WHEN** seed generation completes for a category
- **THEN** the seed titles SHALL cover at least 4 different hook types (question, number-list, controversy, emotional story, knowledge gap)

#### Scenario: Avoid near-duplicate titles
- **WHEN** two generated titles have jieba token overlap > 80%
- **THEN** only the higher-scoring title SHALL be retained

### Requirement: Few-shot selection for optimization
The system SHALL select the 3-5 most relevant seed titles from the target category based on keyword overlap with the user's input title, and inject them into the optimization prompt as few-shot examples.

#### Scenario: Select relevant seeds based on user input
- **WHEN** user inputs "5分钟快手早餐教程" with category "美食"
- **THEN** system selects 3-5 food-category seeds whose keywords overlap most with ["快手", "早餐", "教程"], and includes them in the optimization system prompt as "参考以下爆款标题风格"

#### Scenario: No similar seeds found
- **WHEN** no seeds have significant keyword overlap with user's title (< 2 common keywords)
- **THEN** system SHALL fall back to the top 3 highest-scoring seeds from the category as general style reference
