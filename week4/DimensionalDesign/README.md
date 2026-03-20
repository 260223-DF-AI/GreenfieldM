# StreamFlix Dimensional Model Design

## Project Overview
This project designs a dimensional model for **StreamFlix**, a video streaming service.  
The goal is to support analytics for:
- User viewing behavior
- Content performance
- Subscription analytics
- Device analytics

The model follows dimensional modeling best practices using **star schemas**, **surrogate keys**, **denormalized dimensions**, and **slowly changing dimensions (SCDs)** where appropriate.

## Team Members: both critic and developer/designer
- Magan G
- Danielle S

## Project Scope
This design includes 3 core business processes:

1. Viewing Events
2. Subscription Billing
3. Device Quality Monitoring

## Deliverables Included
- `business-processes.md`
- `fact-tables.md`
- `dimension-tables.md`
- `schema-diagram.md`
- `physical-design.md`
- `scd-implementation.sql`
- `peer-review.md`

## Notes
This warehouse is designed for analytics, not transactional processing.  
All dimension tables use surrogate keys, and conformed dimensions are shared where possible across fact tables.