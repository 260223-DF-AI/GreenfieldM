## Part 1: Dataset and table creation
# Task 1.1: Create a dataset - in md file

# Task 1.2: create a partitioned table
-- Use this as a starting point
CREATE OR REPLACE TABLE `bigLab.analytics_lab.sales_partitioned`
PARTITION BY DATE(transaction_date)
CLUSTER BY customer_id
AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE created_at >= '2023-01-01';

# Task 1.3: Create an external table
CREATE OR REPLACE EXTERNAL TABLE `bigLab.analytics_lab.external_example`
OPTIONS (
  format = 'CSV',
  uris = ['gs://cloud-samples-data/bigquery/us-states/us-states.csv'],
  skip_leading_rows = 1
);

SELECT *
FROM `bigLab.analytics_lab.external_example`
LIMIT 10;

## Part 2: SQL queries
# Task 2.1: basic aggregation
WITH monthly_orders AS (
    SELECT FORMAT_DATE('%Y-%m', DATE(created_at)) AS order_month,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(sale_price) AS total_revenue
    FROM 'bigquery-public-data.thelook_ecommerce.order_items'
    WHERE  DATE(created_at) >= '2023-01-01'
        AND DATE(created_at) < '2024-01-01'
    GROUP BY order_month
)
SELECT order_month, total_orders, total_revenue, 
    SAFE_DIVIDE(total_revenue,total_orders) AS avg_order_value
FROM monthly_orders
ORDER BY order_month;

# Task 2.2: window functions
WITH daily_revenye AS (
    SELECT DATE(created_at) AS order_date, SUM(sale_price) AS daily_revenue
    FROM 'bigquery-public-date.thelook_ecommerce.order_items'
    GROUP BY order_date
)
SELECT order_date, daily_revenue, SUM(daily_revenue) OVER (
    ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total_revenue
FROM daily_revenue ORDER BY order_date;

WITH daily_orders AS (
    SELECT DATE(created_at) AS order_date, COUNT(DISTINCT order_id) AS daily_order_count
    
)

# Task 2.3: ARRAY and STRUCT
SELECT 
    order_id,
    ARRAY_AGG(STRUCT(product_id, sale_price)) AS items
FROM `bigquery-public-data.thelook_ecommerce.order_items`
GROUP BY order_id
LIMIT 10;