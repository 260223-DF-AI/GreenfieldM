# Unified Healthcare Analytics Platform Architecture

## ASCII Architecture Diagram

                        +----------------------+
                        |   Dataset A          |
                        |   Patient Records    |
                        |   PostgreSQL Export  |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        | Batch / CDC Ingestion|
                        +----------+-----------+

                        +----------------------+
                        |   Dataset B          |
                        |   Medical Images     |
                        |   DICOM Files        |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        | File Ingestion Layer |
                        +----------+-----------+

                        +----------------------+
                        |   Dataset C          |
                        |   Doctor Notes       |
                        | PDF / Word Docs      |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        | Document Ingestion   |
                        | + OCR / Text Extract |
                        +----------+-----------+

                        +----------------------+
                        |   Dataset D          |
                        |   IoT Sensor Data    |
                        |   JSON Streams       |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        | Streaming Ingestion  |
                        | (Kafka / PubSub)     |
                        +----------+-----------+

                        +----------------------+
                        |   Dataset E          |
                        |   Insurance Claims   |
                        |   XML Files          |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        | Batch Partner Import |
                        +----------+-----------+
                                   |
                                   v
        ----------------------------------------------------------------
                                   |
                                   v
                        +----------------------+
                        |     Raw Data Lake    |
                        | Object Storage       |
                        | - DICOM              |
                        | - PDF/DOCX           |
                        | - JSON               |
                        | - XML                |
                        | - Raw exports        |
                        +----------+-----------+
                                   |
                                   v
                        +----------------------+
                        | Processing / ETL     |
                        | - Validation         |
                        | - Cleansing          |
                        | - OCR / NLP          |
                        | - Schema Mapping     |
                        | - Stream Processing  |
                        +----------+-----------+
                                   |
                -----------------------------------------------
                |                      |                      |
                v                      v                      v
    +--------------------+  +--------------------+  +--------------------+
    | Curated Data Lake  |  | Data Warehouse     |  | ML / Feature Store |
    | Parquet / Avro     |  | Structured tables  |  | Image + text + IoT |
    +---------+----------+  +---------+----------+  +---------+----------+
              |                       |                       |
              ------------------------------------------------
                                   |
                                   v
                        +----------------------+
                        | Analytics Layer      |
                        | - BI Dashboards      |
                        | - SQL Queries        |
                        | - Clinical Reporting |
                        | - Claims Analysis    |
                        | - Predictive Models  |
                        +----------------------+

## Architecture Explanation

All five datasets first enter an ingestion layer based on how they arrive: batch, file upload, document extraction, partner import, or streaming ingestion. The raw data is stored in a central data lake so the company keeps the original source files for auditability, compliance, and reprocessing.

Next, ETL and stream-processing jobs clean, validate, transform, and enrich the data. Structured and analytics-ready data is written into curated Parquet/Avro zones and a data warehouse, while image, text, and sensor data can also feed machine-learning pipelines and advanced analytics tools.