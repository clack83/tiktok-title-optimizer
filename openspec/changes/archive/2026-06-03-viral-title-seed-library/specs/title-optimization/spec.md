## ADDED Requirements

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
