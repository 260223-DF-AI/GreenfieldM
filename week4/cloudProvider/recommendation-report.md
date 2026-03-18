# Cloud Provider Recommendation Report

## 1. Executive Summary

After comparing AWS, Azure, and Google Cloud for the company’s planned data-platform migration, I recommend **Google Cloud Platform (GCP)** as the best overall fit for this specific use case. GCP offers a strong combination of simple managed analytics through BigQuery, solid object storage, a managed PostgreSQL option through Cloud SQL, and a clear path to future real-time fraud analytics with Dataflow.

## 2. Evaluation Criteria

The five main factors considered were:

1. Fit for managed PostgreSQL workloads
2. Strength of the analytics and data warehouse platform
3. Cost for storage and general-purpose compute
4. Simplicity of operating batch and streaming data pipelines
5. Long-term support for real-time analytics and fraud detection

## 3. Provider Comparison

### AWS

**Strengths:**
- Very broad service catalog with mature enterprise adoption
- Strong managed PostgreSQL support through Amazon RDS
- Strong object storage through Amazon S3
- Good path from batch ETL to streaming analytics with Glue and Managed Service for Apache Flink

**Weaknesses:**
- Service sprawl can make architecture more complex for mid-sized teams
- Analytics often requires combining multiple AWS services instead of relying on one very simple warehouse experience
- Storage costs in this rough estimate were higher than Azure and GCP

### Azure

**Strengths:**
- Strong fit for organizations already invested in Microsoft tools and identity
- Azure Synapse, Blob Storage, and Stream Analytics integrate well inside the Microsoft ecosystem
- Good managed PostgreSQL offering

**Weaknesses:**
- Pricing and service selection can be less straightforward for smaller teams
- In this estimate, compute costs were the highest of the three
- Synapse is capable, but many teams find it less simple than BigQuery for quick warehouse adoption

### GCP

**Strengths:**
- BigQuery is especially strong for analytics because it is highly managed and simple to operate
- Dataflow supports both batch and streaming pipelines, which is useful for the company’s future fraud-detection plans
- Cloud Storage is straightforward and widely used for data lakes and object storage
- In this estimate, GCP had the lowest total rough monthly cost

**Weaknesses:**
- Some organizations have less internal familiarity with GCP than AWS or Azure
- Cloud SQL is strong, but AWS’s database ecosystem is broader overall
- Teams that want a huge marketplace of adjacent services may still prefer AWS

## 4. Recommendation

I recommend **GCP**.

The main reason is that the company’s roadmap is analytics-heavy. They need a managed PostgreSQL database today, but they also need a warehouse for BI, batch pipelines for inventory, object storage for images and customer documents, and later real-time fraud analytics. BigQuery gives them a very strong analytics core, Dataflow covers both batch and streaming use cases, and Cloud Storage provides a simple object-storage foundation. Together, these services create a cleaner and easier-to-operate architecture than the likely AWS or Azure equivalents for a mid-sized retailer.

AWS would be my second choice, especially if the team already has strong AWS skills or expects to build a more customized platform. Azure would be the best choice mainly if the company is already deeply invested in Microsoft 365, Entra ID, Power BI, or other Microsoft enterprise tooling.

## 5. Migration Considerations

1. **Data migration complexity:** Moving PostgreSQL data, historical files, and warehouse-ready datasets from on-premises systems to the cloud will require careful validation, schema mapping, and cutover planning.

2. **Cost control during migration:** Temporary duplication of storage, test environments, and data transfer charges can raise costs during the migration period even if steady-state cloud costs are reasonable.

3. **Security and compliance:** Customer documents, product assets, and transactional data will require strong IAM design, encryption, retention controls, and auditing from the start.

4. **Pipeline redesign:** Existing on-prem batch jobs may need to be redesigned to fit managed cloud-native services rather than simply lifted and shifted.

5. **Team enablement:** The team will need training on the selected provider’s data stack, especially around warehouse design, IAM, monitoring, and incident response.