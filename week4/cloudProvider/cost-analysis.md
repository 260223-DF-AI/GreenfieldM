# Cost Analysis

## Assumptions

To keep the comparison consistent, these estimates assume:

- On-demand/list pricing
- Roughly one month of usage
- No discounts, reserved capacity, or free tiers
- No network egress, API request, backup, or redundancy charges
- One general-purpose Linux VM equivalent for compute

Because the providers price these services differently, this is an approximation for comparison, not a production bill forecast.

## Monthly Estimate Table

| Cost Item | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| 500 GB data warehouse storage | $12.00 | $11.50 | $11.50 |
| 10 TB object storage | $235.52 | $184.32 | $204.80 |
| 1000 compute hours/month | $83.50 | $133.00 | $89.80 |
| **Estimated total** | **$331.02** | **$328.82** | **$306.10** |

## How the estimates were calculated

### AWS

- **Data warehouse storage:** Amazon Redshift managed storage example shows **$0.024 per GB-month** in US East (N. Virginia).  
  500 GB × $0.024 = **$12.00**
- **Object storage:** Amazon S3 Standard example pricing shows **$0.023 per GB-month** for the first 50 TB.  
  10,240 GB × $0.023 = **$235.52**
- **Compute:** Amazon EC2 T3 Large Linux in US East (N. Virginia) shows **$0.0835/hour**.  
  1000 hours × $0.0835 = **$83.50**

### Azure

- **Data warehouse storage:** Azure Synapse Analytics storage is listed at **$23 per TB per month**.  
  0.5 TB × $23 = **$11.50**
- **Object storage:** Azure Blob Storage pricing snippet shows a public **Hot tier example at $0.018 per GB**.  
  10,240 GB × $0.018 = **$184.32**
- **Compute:** Using a 2 vCPU / 8 GB general-purpose VM proxy, Azure pricing on an official Microsoft pricing page shows **D2as v5 at $0.133/hour**.  
  1000 hours × $0.133 = **$133.00**

### GCP

- **Data warehouse storage:** BigQuery active logical storage in us-central1 is listed at **$0.000031507 per GiB-hour**, with an example showing **1 TiB for a full month = $23.552**.  
  500 GiB × $0.000031507 × 730 hours ≈ **$11.50**
- **Object storage:** Google Cloud Storage Standard regional pricing examples show **$0.020 per GB** in a representative regional case.  
  10,240 GB × $0.020 = **$204.80**
- **Compute:** Google Cloud general-purpose pricing shows **c4a-standard-2 at $0.0898/hour**.  
  1000 hours × $0.0898 = **$89.80**

## Sources Used

### AWS
- AWS Pricing Calculator
- Amazon RDS for PostgreSQL pricing
- Amazon Redshift pricing
- Amazon S3 pricing
- Amazon EC2 pricing / T3 instance pricing

### Azure
- Azure Pricing Calculator
- Azure Database for PostgreSQL Flexible Server pricing
- Azure Synapse Analytics pricing
- Azure Blob Storage pricing
- Azure VM pricing references

### GCP
- Google Cloud Pricing Calculator
- Cloud SQL pricing
- BigQuery pricing
- Cloud Storage pricing
- Compute Engine pricing