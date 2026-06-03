# optimization-history Specification

## Purpose
TBD - created by archiving change init-title-optimizer. Update Purpose after archive.
## Requirements
### Requirement: Save optimization record
The system SHALL persist every optimization result, including original title, optimized variations, scores, strategy used, and timestamp.

#### Scenario: Auto-save after optimization
- **WHEN** a successful title optimization completes
- **THEN** system SHALL automatically save a record with original_title, results, scores, strategy, and created_at

### Requirement: Query optimization history
The system SHALL allow users to query their optimization history with pagination and filtering by date range.

#### Scenario: Query recent history
- **WHEN** user requests history with defaults (page=1, page_size=20)
- **THEN** system returns up to 20 most recent optimization records ordered by created_at DESC

#### Scenario: Filter by date range
- **WHEN** user requests history with start_date=2024-01-01 and end_date=2024-01-31
- **THEN** system returns only records within the specified date range

### Requirement: History comparison
The system SHALL allow users to compare two optimization records side by side, showing score deltas and strategy differences.

#### Scenario: Compare two records
- **WHEN** user requests comparison of record IDs A and B
- **THEN** system returns side-by-side diff showing original_title, best_result, overall_score, strategy for each record

### Requirement: Delete history record
The system SHALL allow users to delete individual optimization history records.

#### Scenario: Delete a record
- **WHEN** user deletes history record with valid ID
- **THEN** system soft-deletes the record and returns HTTP 204

#### Scenario: Delete non-existent record
- **WHEN** user tries to delete a record that doesn't exist or belongs to another user
- **THEN** system returns HTTP 404 with message "记录不存在"

