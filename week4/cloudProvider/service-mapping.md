# Cloud Provider Service Mapping

| Requirement | AWS Service | Azure Service | GCP Service |
|-------------|-------------|---------------|-------------|
| Managed PostgreSQL | Amazon RDS for PostgreSQL | Azure Database for PostgreSQL Flexible Server | Cloud SQL for PostgreSQL |
| Data Warehouse | Amazon Redshift | Azure Synapse Analytics | BigQuery |
| Batch Processing | AWS Glue | Azure Data Factory | Dataproc |
| Object Storage | Amazon S3 | Azure Blob Storage | Cloud Storage |
| Stream Processing | Amazon Managed Service for Apache Flink | Azure Stream Analytics | Dataflow |

## Notes

- Amazon RDS for PostgreSQL, Azure Database for PostgreSQL Flexible Server, and Cloud SQL for PostgreSQL are each managed PostgreSQL offerings from their respective providers.
- Amazon Redshift, Azure Synapse Analytics, and BigQuery are the main analytics warehouse platforms for large-scale reporting and BI workloads.
- AWS Glue, Azure Data Factory, and Dataproc all support scheduled batch pipelines, though they differ in how much code and cluster management they require.
- Amazon S3, Azure Blob Storage, and Cloud Storage are the core object stores for images, files, and documents.
- For real-time fraud detection later on, Amazon Managed Service for Apache Flink, Azure Stream Analytics, and Dataflow are strong stream-processing choices.