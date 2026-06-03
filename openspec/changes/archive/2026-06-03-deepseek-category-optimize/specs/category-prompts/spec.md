## ADDED Requirements

### Requirement: Category list query
The system SHALL provide a list of preset content categories, each with name, icon identifier, description, and applicable audience description.

#### Scenario: Get all categories
- **WHEN** frontend requests category list via GET /api/v1/categories
- **THEN** system returns an array of categories including 游戏, 生活, 旅行, 婚恋, 美食, 科技, 职场, 美妆, 健身, 教育

#### Scenario: Category response structure
- **WHEN** a category is returned
- **THEN** each category SHALL contain fields: id, name, icon, description, audience

### Requirement: Category-specific prompt injection
The system SHALL inject category-specific viral keywords, hook patterns, and audience preferences into the LLM system prompt when a category is selected.

#### Scenario: Gaming category optimization
- **WHEN** user selects category "游戏" and submits a title for optimization
- **THEN** the system prompt SHALL include gaming-specific context ("18-30岁男性", "操作/攻略/上分", "钩子: 学会这招直接...") and generated titles SHALL use gaming-appropriate language

#### Scenario: No category selected
- **WHEN** user does not select a category
- **THEN** system SHALL use a general-purpose prompt without vertical-specific optimization

#### Scenario: Lifestyle category with emoji preference
- **WHEN** user selects category "生活"
- **THEN** the prompt SHALL instruct the LLM to prefer warm, relatable language and life-scene emojis (🏠🔥✨)

### Requirement: Category configuration management
The system SHALL store category definitions in a YAML configuration file that supports hot-reload without service restart.

#### Scenario: Update category config
- **WHEN** `categories.yaml` is modified on disk
- **THEN** GET /api/v1/categories SHALL return updated category data within 60 seconds without server restart

#### Scenario: Invalid category config
- **WHEN** `categories.yaml` contains malformed YAML
- **THEN** system SHALL log an error and continue serving the last valid cached configuration

### Requirement: Hook pattern templates per category
Each category SHALL define at least 5 viral hook pattern templates that represent common successful title structures in that vertical.

#### Scenario: Gaming hook patterns
- **WHEN** querying the "游戏" category hook patterns
- **THEN** the category SHALL include patterns like "学会这招直接{action}", "90%的玩家不知道{secret}", "{number}个{character}你必须知道的技巧"

#### Scenario: Relationships hook patterns
- **WHEN** querying the "婚恋" category hook patterns
- **THEN** the category SHALL include patterns like "TA这样对你说明{insight}", "{number}个信号说明TA{conclusion}"
