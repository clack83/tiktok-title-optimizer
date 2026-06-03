# user-management Specification

## Purpose
TBD - created by archiving change init-title-optimizer. Update Purpose after archive.
## Requirements
### Requirement: User registration
The system SHALL allow users to register with email and password, storing credentials securely using bcrypt hashing.

#### Scenario: Successful registration
- **WHEN** user submits valid email "user@example.com" and password "StrongPass123!"
- **THEN** system creates account and returns JWT access token and refresh token

#### Scenario: Duplicate email
- **WHEN** user registers with an email that already exists
- **THEN** system returns HTTP 409 with message "该邮箱已被注册"

#### Scenario: Weak password
- **WHEN** user submits password shorter than 8 characters
- **THEN** system returns HTTP 422 with message "密码长度不能少于8位"

### Requirement: User login
The system SHALL authenticate users with email and password, returning JWT tokens for subsequent API access.

#### Scenario: Successful login
- **WHEN** user submits correct email and password
- **THEN** system returns JWT access_token (expires 1 hour) and refresh_token (expires 30 days)

#### Scenario: Invalid credentials
- **WHEN** user submits wrong password
- **THEN** system returns HTTP 401 with message "邮箱或密码错误"

### Requirement: Token refresh
The system SHALL support refreshing access tokens using a valid refresh token.

#### Scenario: Refresh with valid token
- **WHEN** user submits valid refresh token
- **THEN** system returns new access_token and refresh_token pair

#### Scenario: Refresh with expired token
- **WHEN** user submits expired refresh token
- **THEN** system returns HTTP 401 with message "登录已过期，请重新登录"

### Requirement: User preferences
The system SHALL allow users to save and retrieve optimization preferences including default strategy, preferred title length range, and content category.

#### Scenario: Save preferences
- **WHEN** user submits preferences {default_strategy: "hook_enhancement", max_title_length: 60, category: "美妆"}
- **THEN** system stores preferences and returns updated preference object

#### Scenario: Optimization uses saved preferences
- **WHEN** user with saved preferences submits a title for optimization
- **THEN** system SHALL apply user's default_strategy and length constraints automatically

