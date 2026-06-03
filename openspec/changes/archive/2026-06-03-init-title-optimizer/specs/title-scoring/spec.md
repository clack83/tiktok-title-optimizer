## ADDED Requirements

### Requirement: Core scoring engine
The system SHALL provide a multi-dimensional title scoring engine that evaluates titles across four dimensions: attractiveness (40%), informativeness (25%), readability (20%), and platform fit (15%).

#### Scenario: Score a valid title
- **WHEN** user submits title "这绝对是今年最炸裂的干货分享"
- **THEN** system returns a score object with overall_score (0-100) and dimension_scores for attractiveness, informativeness, readability, platform_fit

#### Scenario: Score an empty title
- **WHEN** user submits an empty string
- **THEN** system returns HTTP 422 with error message "标题不能为空"

#### Scenario: Score a title exceeding max length
- **WHEN** user submits a title longer than 200 characters
- **THEN** system returns HTTP 422 with error message "标题长度不能超过200字"

### Requirement: Attractiveness scoring
The system SHALL calculate attractiveness score based on hook strength, curiosity triggers, emotional impact, and use of power words.

#### Scenario: High attractiveness title
- **WHEN** title contains strong hooks ("绝了", "万万没想到", "99%的人不知道") and emotional triggers
- **THEN** attractiveness score SHALL be >= 70

#### Scenario: Flat descriptive title
- **WHEN** title is purely descriptive without emotional triggers ("今天做了红烧肉的做法教程")
- **THEN** attractiveness score SHALL be < 50

### Requirement: Informativeness scoring
The system SHALL calculate informativeness score based on keyword density, topic relevance, content promise clarity, and specificity.

#### Scenario: Information-rich title
- **WHEN** title contains specific numbers, clear topics, and concrete promises ("3个方法让你7天内涨粉1000")
- **THEN** informativeness score SHALL be >= 70

### Requirement: Readability scoring
The system SHALL calculate readability score based on length appropriateness, proper word segmentation, no ambiguity, and good formatting.

#### Scenario: Overly long title
- **WHEN** title exceeds 80 characters
- **THEN** readability score SHALL be reduced proportionally

#### Scenario: Well-formatted title
- **WHEN** title uses proper punctuation and clear structure
- **THEN** readability score SHALL be >= 70

### Requirement: Platform fit scoring
The system SHALL calculate platform fit score based on emoji usage, hashtag strategy, and format compliance with TikTok best practices.

#### Scenario: Title with relevant emojis and hashtags
- **WHEN** title includes 1-3 relevant emojis and 2-5 targeted hashtags
- **THEN** platform_fit score SHALL be >= 75

#### Scenario: Title with no hashtags
- **WHEN** title has zero hashtags
- **THEN** platform_fit score SHALL be < 50

### Requirement: Score explanation
The system SHALL provide human-readable explanations for each dimension score, describing why the score was assigned.

#### Scenario: Get score with explanations
- **WHEN** user requests a title score
- **THEN** response includes `explanations` object with brief Chinese explanations for each dimension
