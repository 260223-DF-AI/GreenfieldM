## Physical Design Consideration - Part 3

## 1. fact_user_viewing_behavior
### Partitioning Strategy
Partition by **viewing date** using 'date_key'

This table stores one row per viewing session, making it very high volume.  Most queries filter by time (day, week, month), so date-based partitioning improves performance and reduces scan cost.

### Clustering Columns
- 'session_id'
- 'user_id'
- 'content_id'
- 'content_title'
- 'content_category'

These columns support queries like:
- most watched content
- viewing by region
- device usage trends
- user engagement analysis

### Estimated Table Size and Growth Rate
- about 50 million rows per month
- growth rate: 10-20% per quarter

### Recommended Load Frequency
- micro-batches ever **5-15 minutes**

## 2. fact_subscription_analytics
### Partitioning Strategy
Partition by **transaction date** using 'date_key

Revenue and billing queries are time-based (monthly revenue, churn, etc.), so date partitioning improves performance.

### Clustering Columns
- 'billing_id'
- 'user_id'
- 'billing_date'
- 'payment_method'
- 'plan_type'
- 'plan_rate'
- 'amount_paid'
- 'plan_status'
- 'activation_date'
- 'cancellation_date

Supports analysis such as:
- revenue by plan
- churn by region
- payment behavior
- subscription trends

### Estimated Table Size and Growth Rate
- about 2 million rows per month
- growth rate: 5-10% per quarter

### Recommended Load Frequency
- **hourly or daily**

## 3. fact_device_analytics
### Partitioning Strategy
Partition by **event date** using date_key

This table contains high volume telemetry data.  Most queries docus on recent time periods, making date partitioning essential.

### Clustering Columns
- 'device_id'
- 'session_id'
- 'user_id'
- 'device_type'
- 'network_type'
- 'region'
- 'playback_speed'
- 'playback_quality'
- 'buffering_time'
- 'media_file_size'

Supports analysis such as:
- buffering by device
- network performance
- quality by content
- regional playback issues

### Estimated Table Size and Growth Rate
- about 200 million rows per month
- growth rate: 15-25% per quarter

### Recommended Load Frequency
- streaming for micro-batches ever **1-5 minutes**

## 4. Dimension Table Design Notes 
### dimUser
- Cluster: 'user_id', 'current_flag'
- Load: daily or incremental updates
### dimContent
- Cluster: 'content_id', 'genre', 'current_flag'
- Load:  daily or on catalog updates
### dimDevice
- Cluster: 'device_id', 'device_type', 'current_flag'
- Load: daily
### dimSubscriptionPlan
- Cluster: 'plan_id', 'current_flag'
- Load: on plan/pricing changes
### dimGeography
- Cluster: small table, no partitioning needed
- Load/refresh: weekly or as needed

Other tables (date, payment method, promotion, network) aren't needing additional design notes.  Not being used/shown directly.

## 5. Final Notes
This physical design:
- imporves query performance
- reduces data scan cost
- supports time based analytics
- scales with increasing user activity
In production, these strategies would be refined based on actual usage patterns and system performance metrics.