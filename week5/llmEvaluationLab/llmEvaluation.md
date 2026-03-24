## LLM EVALUATION LAB - MARCH 24
## PART 1 - ACCURACY EVALUATION
### 1.1: SQL ACCURACY CHECK
| Criterion | Score (1-5) | Notes |
| --------- | ----------- | ----- |
| Syntax correctness (valid BigQuery SQL) | | |
| Window function usage (correct frame clause) | | |
| Rolling average logic (correct 7-day calculation) | | |
| Column references match the provided schema | | |
| Overall: would this query run correctly? | | |

1. Check that the window frame specifies the correct range (6 PRECEDING AND CURRENT ROW or equivalent)
2. Verify the function used is AVG, not SUM
3. Confirm DATE ordering is correct
4. Look for any BigQuery-specific syntax issues

### 1.2: FACT CHECK

| Statement from LLM | Verified? (Yes/No/Unsure) | Source Used to Verify |
| ------------------- | ------------------------- | --------------------- |

Use the [BigQuery documentation](https://cloud.google.com/bigquery/docs/storage_overview) to verify at least 3 claims made by the LLM. Document which claims are accurate and which appear to be hallucinated.


## PART 2 - HALLUCINATION DETECTION
### 2.1: API HALLUCINATION HUNT

1. Read through the generated code carefully
2. Look for:
   - Function names that do not exist in the BigQuery Python client
   - SQL syntax that is not valid BigQuery ML syntax
   - Configuration options that do not exist
   - Import statements for non-existent modules
3. Verify against the [BigQuery ML documentation](https://cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create)

**Document your findings:**

| Item | LLM Generated | Actual (from docs) | Hallucination? |
| ---- | ------------- | ------------------- | -------------- |

### 2.2: CITATION VERIFICATION
1. Attempt to verify each citation
2. Search for the paper title online
3. Does it exist? Are the authors correct? Is the year correct?
4. Document your findings


## PART 3 - COMPARATIVE EVALUATION
### 3.1: SAME PROMPT, DIFF APPROACH

| Criterion | Zero-shot Output | Constrained Output |
| --------- | ---------------- | ------------------ |
| Correctness | | |
| Completeness | | |
| Edge case handling | | |
| Code quality | | |
| Would you use this in production? | | |

### 3.2: SAFETY AND BOUNDARIES
1. How did the model handle each prompt?
2. Did it provide useful security information while maintaining appropriate boundaries?
3. Was the response helpful for legitimate security work?


## PART 4 - REFLECTION AND SCORING
### OVERALL MODEL ASSESSMENT 

Based on all exercises above, rate the LLM you used:

| Category | Score (1-10) | Justification |
| -------- | ------------ | ------------- |
| SQL generation accuracy | | |
| Factual reliability | | |
| Hallucination frequency | | |
| Safety and boundaries | | |
| Response to constraints | | |
| Overall usefulness for data engineering | | |


1. What was the most surprising hallucination you found?
2. In which category did the LLM perform best? Worst?
3. How would you change your AI usage habits based on this evaluation?
4. What verification steps would you add to your daily workflow?
5. Would you trust the LLM to generate production SQL without review? Why or why not?
