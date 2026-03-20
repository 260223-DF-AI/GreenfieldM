# Fact Tables

## User Viewing Behavior
### What content is being watched, when, and for how long
**Table type**: Transaction

**Table name**: fact_viewing_sessions
**Grain statement**: Each row represents one complete viewing session by a user for a specific content title on a specific device at a certain date and time.

Columns:
- session_key (PK)
- session_id
- user_key (FK -> dim_user)
- content_key (FK -> dim_content)
- device_key (FK -> dim_device)
- date_key (FK -> dim_date)
- viewing_duration_minutes
- viewing_duration_seconds
- content_category
- subscription_plan_key (FK -> dim_subscription_plan)
- completion_rate_pct
- watch_percentage
- session_start_time
- session_end_time
- pause_count
- resume_count
- device_type
- dw_insert_date
- dw_update_date

Measures:
- Additive:
    - viewing_duration_minutes
    - viewing_duration_seconds
- Semi-additive:
    - (none stored as true semi-additive in this table; all are per-session values)
- Non-additive:
    - completion_rate_pct
    - watch_percentage

## Subscription Analytics 
### User acquisition, churn, and revenue analysis
**Table type**: Periodic Snapshot

**Table name**: fact_subscription_payments
**Grain statement**: Each row represents one billing snapshot transaction for a user subscription event (month-end or cycle-end).

Columns:
- billing_key (PK)
- billing_id
- user_key (FK -> dim_user)
- subscription_plan_key (FK -> dim_subscription_plan)
- payment_method_key (FK -> dim_payment_method)
- geography_key (FK -> dim_geography)
- date_key (FK -> dim_date)
- amount_paid
- new_subscriber_flag
- monthly_subscription_count
- payment_method_count
- active_subscriber_count
- plan_rate
- plan_price_usd
- plan_status
- plan_tier
- payment_type
- activation_date
- cancellation_date
- churn_flag
- dw_insert_date
- dw_update_date

Measures:
- Additive:
    - amount_paid
    - new_subscriber_flag
    - monthly_subscription_count
    - payment_method_count
- Semi-additive:
    - active_subscriber_count
    - plan_rate
- Non-additive:
    - plan_price_usd
    - churn_flag

## Device Analytics
### Which devices are used, streaming quality metrics
**Table type**: Transaction

**Table name**: fact_devices
**Grain statement**: Each row represents one device telemetry event for a viewing session by a user.

Columns:
- device_event_key (PK)
- device_session_id
- device_key (FK -> dim_device)
- user_key (FK -> dim_user)
- network_key (FK -> dim_network)
- geography_key (FK -> dim_geography)
- date_key (FK -> dim_date)
- playback_failure_count
- buffering_duration_seconds
- buffer_event_count
- playback_event_count
- playback_quality_event_count
- rebuffer_event_count
- dropped_frames_count
- session_count
- unique_device_count
- device_count_per_user
- playback_failure_rate
- avg_session_duration_seconds
- avg_buffer_duration_sec
- avg_bitrate_kbps
- playback_quality_pct
- abandonment_rate
- playback_speed
- playback_quality
- device_type
- network_type
- media_file_size
- session_abandonment_flag
- dw_insert_date
- dw_update_date

Measures:
- Additive:
    - playback_failure_count
    - buffering_duration_seconds
    - buffer_event_count
    - playback_event_count
    - playback_quality_event_count
    - rebuffer_event_count
    - dropped_frames_count
    - session_count
- Semi-additive:
    - unique_device_count
    - device_count_per_user
- Non-additive:
    - playback_failure_rate
    - avg_session_duration_seconds
    - avg_buffer_duration_sec
    - avg_bitrate_kbps
    - playback_quality_pct
    - abandonment_rate
