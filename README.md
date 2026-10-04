Sales Agent

Lead discovery and qualification pipeline for small B2B businesses. Built construction-supply business in rural Ireland, designed to be reused by other businesses through configuration alone.

Status: in development. Discovery, storage and deduplication work. AI qualification and outreach are next.

What it does now
- Discovers local businesses (builders, electricians, hardware suppliers etc.) from OpenStreetMap within a configurable radius
- Stores companies and sales leads in PostgreSQL, with company data kept separate from lead/sales data
- Deduplicates prospects by normalised name + location, phone number, or website, so re-runs and messy source data don't create duplicate leads
- Exposes companies and leads through a REST API (FastAPI)

Architecture
Data
Business data © OpenStreetMap contributors, available under the Open Database License (ODbL).
