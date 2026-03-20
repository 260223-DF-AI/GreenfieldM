## Physical Design Consideration - Part 3

## 1. fact_viewing_session
### Partitioning Strategy
Partition by **viewing date** using 'date_key'

This table stores one row per viewing session, making it very high volume.  Most queries filter by time (day, week, month), so date-based partitioning improves performance and reduces scan cost.

### Clustering Columns
- 'content_key'
- 'user_key'
- 'device_key'
- 'geography_key'

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

## 2. fact_subscription_transaction
### Partitioning Strategy
Partition by **transaction date** using 'date_key

Revenue and billing queries are time-based (monthly revenue, churn, etc.), so date partitioning improves performance.

### Clustering Columns
- 'subscription_plan_key'
- 'user_key'
- 'geography_key'
- 'payment_method_key'

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

## 3. fact_playback_quality_event
### Partitioning Strategy

### Clustering Columns

### Estimated Table Size and Growth Rate

### Recommended Load Frequency

## 4. Dimension Table Design Notes
### Partitioning Strategy

### Clustering Columns

### Estimated Table Size and Growth Rate

### Recommended Load Frequency

## 5. Final Notes