# Classification Table

| Dataset | Data Type | Volume | Velocity | Variety | Veracity Concerns |
|---------|-----------|--------|----------|---------|-------------------|
| A | Structured | High (50 GB) | High - real-time inserts plus daily batch updates | Low to moderate - mostly relational tables such as demographics, visits, and billing codes | Missing values, duplicate patient records, incorrect billing codes, outdated patient information |
| B | Unstructured | Very high (5 TB) | Moderate to high - continuous image generation (100+ images/hour) | High - multiple image types such as X-rays, MRIs, and CT scans | Corrupted files, inconsistent image quality, missing metadata, patient-to-image matching errors |
| C | Unstructured | High (200 GB) | Moderate - daily additions | High - PDFs, Word documents, typed notes, handwritten prescriptions | Illegible handwriting, incomplete notes, OCR errors, inconsistent terminology, document duplication |
| D | Semi-structured | Very high (10 GB/day) | Very high - real-time streaming at 1000 events/second | Moderate to high - JSON with different device payloads and sensor readings | Noisy readings, device malfunctions, missing fields, timestamp drift, duplicate events |
| E | Semi-structured | Moderate (2 GB/week) | Low - weekly batch | Moderate - XML with nested claims, approvals, and denials | Schema inconsistencies across partners, missing tags, invalid claim codes, duplicate claims, partner data quality issues |