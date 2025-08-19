# Personal Data Organizer

## Problem
I’m migrating from Windows to Linux with a large, mixed, and sensitive personal dataset.  
I need a safe, reproducible pipeline to inventory, organize, deduplicate, and enrich files (images, docs, binaries) and to detect/handle sensitive info (e.g., CURP, credentials).

## Success metrics
- 100% files inventoried with hashes and mimetypes
- ≥95% correct routing into high-level types (images/docs/archives/binaries)
- Zero in-place modification during inventory/staging
- Duplicate detection reduces storage by ≥20%
- PII detector achieves ≥90% precision on a labeled subset

## Constraints
- Read-only until staging is verified
- No raw sensitive data in GitHub/DVC
- Logs & reports exclude secrets

## Deliverables
Inventory catalog, staging tree, dedupe report, enrichment features, PII tags, FastAPI microservice, documentation
