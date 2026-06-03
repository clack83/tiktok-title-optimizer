# keyword-analysis Specification

## Purpose
TBD - created by archiving change init-title-optimizer. Update Purpose after archive.
## Requirements
### Requirement: Keyword extraction
The system SHALL extract key keywords and phrases from a title using Chinese NLP segmentation (jieba with custom dictionary).

#### Scenario: Extract keywords from title
- **WHEN** user submits title "新手必看的5个手机摄影技巧"
- **THEN** system returns extracted keywords: ["新手", "手机摄影", "技巧"] with relevance weights

#### Scenario: Handle mixed content title
- **WHEN** title contains Chinese text, numbers, and emojis
- **THEN** system SHALL extract Chinese keywords while preserving numeric information as separate tokens

### Requirement: Popular topic matching
The system SHALL match extracted keywords against a maintained hot-topic database to identify trending opportunities.

#### Scenario: Keyword matches trending topic
- **WHEN** extracted keyword "手机摄影" matches a trending topic
- **THEN** system returns matched topic with trend_score, popularity level (high/medium/low), and suggested hashtags

#### Scenario: No trending match
- **WHEN** no extracted keywords match current trending topics
- **THEN** system returns empty matches and suggests broader keywords to explore

### Requirement: Custom dictionary management
The system SHALL maintain a custom jieba dictionary for TikTok-specific slang, internet buzzwords, and platform-specific terms.

#### Scenario: Recognize TikTok slang
- **WHEN** title contains phrases like "yyds", "破防了", "我悟了"
- **THEN** system SHALL correctly segment these as single tokens using custom dictionary

