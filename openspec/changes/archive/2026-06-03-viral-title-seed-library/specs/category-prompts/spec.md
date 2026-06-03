## ADDED Requirements

### Requirement: Seed preview in category detail
Each category response SHALL include a `seed_preview` field containing the top 3 highest-scoring seed titles for quick browsing in the category selector.

#### Scenario: User sees seed preview while selecting category
- **WHEN** user opens the category dropdown to select "职场"
- **THEN** the dropdown item for "职场" SHALL display seed_count and a hover tooltip showing the top 3 seed titles as style examples
