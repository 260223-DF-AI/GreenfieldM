## Prompt Engineering Lab
### Zero-shot Prompting - PART 1
### 1.1: SQL Generation
Original Prompt: Write a BigQuery SQL query to find the top 5 departments by average salary. Include department name, average salary, and employee count. Only include departments with more than 10 employees. Order by average salary descending.

Refined Prompt: Write a valid BigQuery SQL query for a table named employees with columns department_name, employee_id, and salary. Return the top 5 departments by average salary. Include: department_name, average salary as avg_salary, employee count as employee_count. Only include departments with more than 10 employees. Order by avg_salary descending. Use BigQuery Standard SQL.

Final Output:
SELECT
  department_name,
  AVG(salary) AS avg_salary,
  COUNT(employee_id) AS employee_count
FROM employees
GROUP BY department_name
HAVING COUNT(employee_id) > 10
ORDER BY avg_salary DESC
LIMIT 5;

Evaluation: The refined prompt is better because it names the table, columns, SQL dialect, and expected aliases. That reduces ambiguity and improves correctness.

What you learned?
Zero-shot works well when the task is simple, but adding schema context makes the output much more reliable.

### 1.2: Error Explanation
Original Prompt: Explain this BigQuery error in plain English and suggest a likely fix: "google.api_core.exceptions.BadRequest: 400 Syntax error: Expected end of input but got keyword SELECT at [3:1]" Assume the user is new to SQL. Keep the explanation short and easy to understand.

Final output:
his error means BigQuery found a second SELECT or another unexpected SQL statement where it expected the query to already be finished. In plain English, your SQL is probably structured incorrectly, and BigQuery thinks the query should have ended before line 3.

A likely fix is to check for:

an extra SELECT
a missing comma
a missing closing parenthesis
a subquery that is not written correctly

Start by reviewing line 3 and the line before it.

Evaluation: 
Explanation Accuracy: 5/5
Fix Suggestion Quality: 4/5

What you learned?
For explanation prompts, asking for “plain English” and giving the audience level helps a lot.

### 1.3: Data Dictionary Entry
Original Prompt: Generate a data dictionary entry for a column named customer_lifetime_value in a table called dim_customer.
Include:
data type
description
business definition
calculation method
example values
Write it in a professional format useful for a new data team member.

Final output: 
Table Name: dim_customer
Data Type: NUMERIC(12,2)

Description:
Represents the total revenue attributed to a customer over the full duration of their relationship with the business.

Business Definition:
Customer lifetime value is the cumulative amount of money a customer has spent across all completed purchases.

Calculation Method:
Sum of all completed order amounts associated with the customer, minus refunds if applicable.

Example Values:

0.00
125.50
1899.99

Evaluation: 4/5. This is useful, but it still depends on business rules. For example, whether refunds, taxes, shipping, or canceled orders are included is not fully defined.

What you learned?
Zero-shot can create a strong draft, but business definitions need domain context to be truly accurate.

### Few-shot Prompting - PART 2
### 2.1: Column Name Standardization
Prompt:
Convert column names to snake_case using these examples:

CustomerFirstName -> customer_first_name
order-total-amount -> order_total_amount
PRODUCT ID -> product_id

Now convert these:

ShippingAddress Line1
total_Revenue_YTD
customerEmailAddress
ORDER__STATUS__CODE

Return only the converted names, one per line.

Output:
shipping_address_line1
total_revenue_ytd
customer_email_address
order_status_code

Evaluation:
5/5 The model should handle all four correctly because the examples clearly establish the pattern.

What you learned?
Few-shot prompting is very effective when you want the model to mimic a formatting pattern.

### 2.2: SQL to Documentation
Prompt:
Generate documentation for SQL queries using this format.
SELECT customer_id, COUNT(*) as order_count 
FROM orders GROUP BY customer_id

SELECT p.category, 
       DATE_TRUNC(o.order_date, MONTH) as month,
       SUM(o.quantity * p.unit_price) as revenue,
       COUNT(DISTINCT o.customer_id) as unique_customers
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
GROUP BY 1, 2
ORDER BY 1, 2

Output:
Query: Customer Order Count
Purpose: Counts the total number of orders per customer
Tables Used: orders
Output Columns: customer_id, order_count
Aggregation: COUNT grouped by customer_id

Query: Monthly Revenue and Unique Customers by Product Category
Purpose: Calculates monthly revenue and counts unique customers for each product category starting from January 1, 2024
Tables Used: orders, products
Output Columns: category, month, revenue, unique_customers
Aggregation: SUM of quantity * unit_price and COUNT DISTINCT customer_id grouped by category and month

Evaluation:
5/5
The format is followed well, and the documentation is accurate.

What you learned?
Few-shot prompting is especially useful for documentation, naming conventions, and repeated structured outputs.

### Chain-of-thought Prompting - PART 3
### 3.1: Cost Estimation
Prompt:
Think through this step by step.

Estimate the daily BigQuery query cost for this scenario:

A table has 500 million rows
Each row is approximately 500 bytes
The table has 20 columns
A query scans 3 columns
The query runs 4 times per day
BigQuery charges $6.25 per TB scanned
Assume columnar storage distributes data evenly across columns

Show each calculation step clearly.

Output:
Total table size = 500,000,000 × 500 bytes = 250,000,000,000 bytes = 250 GB
Since the table has 20 columns and storage is evenly distributed, each column is about 250 GB / 20 = 12.5 GB
Query scans 3 columns, so bytes scanned per query = 12.5 GB × 3 = 37.5 GB
Query runs 4 times per day, so daily scanned data = 37.5 GB × 4 = 150 GB
Convert to TB = 150 / 1024 = about 0.1465 TB
Daily cost = 0.1465 × $6.25 = about $0.92 per day

Final Answer: Approximately $0.92 per day

Evaluation:
5/5. The steps are logical and the answer is reasonable. It makes the math transparent and easier to verify.

What you learned?
Chain-of-thought is very helpful for cost estimation, troubleshooting, and multi-step reasoning tasks.

### 3.2: Pipeline Debugging
Prompt:
Think through this step by step.

An ETL pipeline extracts data from a REST API, transforms it with Python, and loads it into BigQuery. It ran successfully for 30 days, then suddenly failed with this error:

google.api_core.exceptions.Forbidden: 403 Access Denied: 
BigQuery BigQuery: Permission bigquery.tables.create denied

Nothing in the pipeline code changed. The GCP project and service account are the same.

Reason through the most likely causes from most likely to least likely. Then recommend what to check first.

Output:
Step-by-step reasoning:

The error is permission-related, not a syntax or data issue.
Since the code did not change, the most likely cause is an infrastructure or IAM change.
The permission specifically denied is bigquery.tables.create, which means the service account can no longer create tables.
Possible causes:
IAM role was removed or changed
dataset-level permissions were changed
pipeline is now writing to a new dataset where permissions are missing
organization policy or security policy changed
a table expiration or cleanup process caused the pipeline to recreate tables, exposing a missing permission that was not needed before

Most likely root cause:
The service account lost a role containing bigquery.tables.create, or the dataset permissions changed.

What to check first:
Check IAM roles for the service account and dataset permissions in BigQuery.

Evaluation:
5/5. The reasoning is logical and grounded in the error message.

Do I agree?
Yes. I would first check:
service account IAM roles
dataset access controls
whether the pipeline is creating new tables instead of appending to existing ones

What you learned?
Chain-of-thought works best when there are multiple possible root causes and I need the model to reason through them.


### Contatraint Application - PART 4
### 4.1: Constained Output
Prompt: 
Write a Python function with all of these constraints:
Function name: validate_order_data
Input: pandas DataFrame
Must check for: null values, negative amounts, future dates, duplicate IDs
Output: a dictionary with check results
Maximum 30 lines of code
Must include type hints
Must include a docstring
No external libraries beyond pandas and datetime

Output:
import pandas as pd
from datetime import datetime

def validate_order_data(df: pd.DataFrame) -> dict:
    """Validate order data for nulls, negative amounts, future dates, and duplicate IDs."""
    results: dict = {}

    results["null_values"] = df.isnull().sum().to_dict()

    if "amount" in df.columns:
        results["negative_amounts"] = int((df["amount"] < 0).sum())
    else:
        results["negative_amounts"] = "amount column missing"

    if "order_date" in df.columns:
        dates = pd.to_datetime(df["order_date"], errors="coerce")
        results["future_dates"] = int((dates > pd.Timestamp(datetime.now())).sum())
    else:
        results["future_dates"] = "order_date column missing"

    if "order_id" in df.columns:
        results["duplicate_ids"] = int(df["order_id"].duplicated().sum())
    else:
        results["duplicate_ids"] = "order_id column missing"

    return results

Evaluation: 
5/5
- Did it satisfy all constraints?
Yes:
correct function name
DataFrame input
checks all requested conditions
dictionary output
under 30 lines
type hints included
docstring included
only uses pandas and datetime
- Which constraints were hardest for the model to follow?
Usually the maximum line count and strict library limitations are the hardest. Without explicitly stating them, models often produce extra helper functions or imports.

What you learned?
Constraints are very powerful when you need production-style output with specific formatting or implementation limits.

### Submission Reflection
### 1. What prompting technique produced the best results for data engineering tasks?
Few-shot and chain-of-thought produced the best results overall.
- Few-shot was strongest for formatting, naming conventions, and documentation.
- Chain-of-thought was strongest for calculations, debugging, and troubleshooting.
- Zero-shot worked best for simpler tasks when the prompt was specific enough.

### 2. What made the biggest difference in output quality: specificity, examples, or constraints?
The biggest difference came from specificity first, then examples, then constraints.
- Specificity reduces ambiguity.
- Examples teach the model the exact pattern you want.
- Constraints help control the final format and quality.

### 3. When would you choose each technique in daily work?'
- Zero-shot: when I need a quick answer for a simple task like writing a query, summarizing an error, or generating a first draft.
- Few-shot: when I need consistent formatting, naming standards, or documentation style.
- Chain-of-thought: when solving multi-step problems like debugging pipelines, estimating costs, or reasoning through architecture decisions.
- Constraint-based prompting: when I need code or documentation to follow strict rules for team or project standards.