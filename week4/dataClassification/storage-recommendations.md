# Storage Recommendations

## Dataset A: Patient Records

**Storage:** Data Warehouse  
**Format:** Parquet  
**Justification:** Patient records are highly structured and frequently queried for reporting, analytics, and operational dashboards. Storing them in a data warehouse using Parquet provides strong compression, fast column-based reads, and efficient SQL analytics for demographics, visit history, and billing trends.

## Dataset B: Medical Images

**Storage:** Object Storage / Data Lake  
**Format:** DICOM  
**Justification:** Medical images are large binary files and should remain in their native DICOM format because that preserves both the image and its embedded medical metadata. Object storage is the best fit because it scales well for massive files, supports cost-effective long-term retention, and works well with downstream AI/ML image processing pipelines.

## Dataset C: Doctor Notes

**Storage:** Data Lake / Object Storage  
**Format:** PDF and DOCX in raw zone, with extracted text as JSON or Parquet for analytics  
**Justification:** Doctor notes are largely unstructured and should first be stored in their original formats to preserve legal and clinical integrity. For analytics, NLP, and search, extracted text can be stored separately in JSON or Parquet so the company can analyze note contents without losing the original source documents.

## Dataset D: IoT Sensor Data

**Storage:** Data Lake with streaming ingestion, plus time-series or analytics layer  
**Format:** Avro or Parquet  
**Justification:** IoT sensor data arrives at very high speed and in semi-structured JSON, so it should be ingested through a streaming pipeline and converted into a more efficient analytics format. Avro is useful during ingestion because it handles schema evolution well, while Parquet is better for downstream analytical queries on large volumes of time-series sensor data.

## Dataset E: Insurance Claims

**Storage:** Data Lake feeding into Data Warehouse  
**Format:** XML in raw zone, transformed to Parquet for analytics  
**Justification:** Claims data comes from external partners in nested XML, so it is important to keep the raw XML for traceability and compliance. After validation and transformation, Parquet is a better format for analytics because it simplifies querying nested claim information and improves performance for batch reporting.