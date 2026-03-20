# Fact Tables

## User Viewing Behavior
### What content is being watched, when, and for how long
**Table type**: Transaction

**Grain statement**: Each row represents a viewing session by a user for a specific content title on a specific device at a particular date and time.

| session_id (PK) | user_id (FK) | content_id (FK) | content_title | content_category | date | duration | device_id (FK) | device_type |
|----|----|----|----|----|----|----|----|----|

---
Measures:
- Additive: 
    - A single user's total viewing minutes
- Semi-additive: 
    - Peak day and time of streaming across all users
    - Current subscribers
    - Current inactive subscribers (haven't streamed in X amount of days)
    - Content category performance by region
    - Total viewing hours per subscription plan
- Non-additive: 
    - Completion percentage
    - Avg watch time per user
    - Avg watch time per content category across all users

## Subscription Analytics 
### User acquisition, churn, and revenue analysis
**Table type**: Periodic Snapshot

**Grain statement**: Each row represents billing transactions per user subscription events.

| billing_id (PK) | user_id (FK) | billing_date | payment_method | plan__type | plan_rate | amount_paid | plan_status | activation_date | cancellation_date | 
|----|----|----|----|----|----|----|----|----|----|

---
Measures:
- Additive: 
    - Total new subscribers per period
    - Count of each payment method
    - Number of users per plan type
- Semi-additive: 
    - Total revenue per plan type
    - Total revenue per month
    - Total revenue per region
- Non-additive: 
    - Churn rate
    - Churn rate per plan type

## Device Analytics
### Which devices are used, streaming quality metrics
**Table type**: Transaction

**Grain statement**: Each row represents the device telemetry for a viewing session by a user 

| device_id (PK) | session_id (FK) | user_id (FK) | device_type | network_type (FK) | region | playback_speed | playback_quality | buffering_time | media_file_size |
|----|----|----|----|----|----|----|----|----|----|

---
Measures:
- Additive: 
    - Count of playback failures per device
    - Counts of playback qualities per region
    - Counts of playback qualities per network type
    - Counts of session per device type
- Semi-additive: 
    - Unique device used
    - Count of devices per user account
- Non-additive: 
    - Playback failure rate
    - Avg session per device
    - Avg buffering time per device
