## MODIFIED Requirements

### Requirement: Score explanation
The system SHALL provide structured diagnostic feedback for each dimension score, including problem diagnosis, recommended improvement direction, and expected effect of the improvement.

#### Scenario: Get score with diagnostic explanations
- **WHEN** user requests a title score
- **THEN** response includes `explanations` object with, for each dimension: `{score, diagnosis, improvement, expected_effect}` - all in Chinese

#### Scenario: Low attractiveness diagnosis
- **WHEN** a title scores < 50 on attractiveness
- **THEN** the attractiveness explanation SHALL include: specific problem diagnosis (e.g., "缺少开头hook"), concrete improvement direction (e.g., "在前8个字加入好奇心钩子"), and expected effect (e.g., "预计吸引力提升15-25分")

#### Scenario: High score diagnostic
- **WHEN** a dimension scores >= 80
- **THEN** the explanation SHALL acknowledge the strength with a positive diagnosis and suggest minor polish if applicable

## ADDED Requirements

### Requirement: Optimization rationale display support
The score explanation structure SHALL be designed to support frontend rendering of expandable diagnostic cards, where each dimension shows a brief score badge initially, and expands to show full diagnosis on click.

#### Scenario: Frontend renders diagnostic card
- **WHEN** frontend receives scoring result with explanations
- **THEN** each dimension card SHALL display: dimension name, score number, color-coded badge, and a one-line summary; clicking the card SHALL expand to show full diagnosis, improvement, and expected_effect

### Requirement: User trust signal in explanations
Explanations SHALL be written to build user confidence by citing specific elements from the user's original title, avoiding generic statements.

#### Scenario: Cited explanation
- **WHEN** user submits title "今天天气真好"
- **THEN** the explanation SHALL reference specific words or patterns from the title (e.g., "标题缺少具体信息和价值点，仅有天气描述") rather than generic feedback (e.g., "标题不够好")
