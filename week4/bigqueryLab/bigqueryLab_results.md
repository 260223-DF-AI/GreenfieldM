# BigQuery Lab Results

## Part 1: Dataset and Table Creation

### Task 1.1: Create a Dataset

```sql
CREATE SCHEMA `analytics_lab`
OPTIONS (
  location = 'US',
  default_table_expiration_days = 7
);