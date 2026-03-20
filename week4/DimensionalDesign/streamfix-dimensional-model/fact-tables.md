# Fact Tables

## User Viewing Behavior
### What content is being watched, when, and for how long
**Table type**: Transaction
**Grain statement**: Each row represents a viewing session by a user for a specific content title on a specific device at a particular date and time.

| session_id (PK) | user_id (FK) | content_id (FK) | content_title | content_category | date | duration | device_id (FK) | device_type |
|----|----|----|----|----|----|----|----|

---
Measures:
- Additive: 
    - A single user's total viewing minutes
    - Avg watch time per user
    - Avg watch time per content category across all users
    - Peak day and time of streaming across all users
- Semi-additive: 
    - Current subscribers
    - Current inactive subscribers (haven't streamed in X amount of days)
    - Content category performance by region
    - Total viewing hours per subscription plan
- Non-additive: 
    - Completion percentage


## Subscription Analytics 
### User acquisition, churn, and revenue analysis

## Device Analytics
### Which devices are used, streaming quality metrics