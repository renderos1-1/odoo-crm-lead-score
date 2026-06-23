# Odoo 17 CRM Lead Score — Cloud Run Demo

A self-hosted **Odoo 17** deployment on Google Cloud with a **custom CRM module** that
adds automatic lead scoring and analytics-friendly banding.

## Architecture

```
Browser ──HTTPS──► Cloud Run (Odoo 17, port 8069)
                       │ unix socket /cloudsql/<conn>
                       ▼
                  Cloud SQL (PostgreSQL 16)
Image built by Cloud Build (FROM odoo:17 + module) ──► Artifact Registry
```

Odoo is a monolithic Python application that serves both the backend and its own
(OWL-based) web frontend, backed exclusively by PostgreSQL.

## Custom module: `crm_lead_score`

Extends the standard `crm.lead` model with two stored, computed fields:

| Field | Description |
|-------|-------------|
| `lead_score` (0–100) | `probability×0.4` + normalised deal size (×40) + contactability (0–20) |
| `score_band` | Hot (≥70) / Warm (40–69) / Cold (<40) — for grouping in pivot/graph views |

```
crm_lead_score/
├── __manifest__.py            # metadata, depends: ['crm']
├── models/crm_lead.py         # _inherit = 'crm.lead', computed field + @api.depends
└── views/crm_lead_views.xml   # xpath view inheritance (form / list / search group-by)
```

## Run locally

```bash
docker run -p 8069:8069 --name odoo-db -e POSTGRES_USER=odoo \
  -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres -d postgres:16
docker build -t odoo-crm .
docker run -p 8069:8069 --link odoo-db:db -t odoo-crm \
  odoo -i crm,sale_management,crm_lead_score
# browse http://localhost:8069  (admin / admin)
```

## Deploy to Cloud Run (summary)

1. Build & push image to Artifact Registry (`gcloud builds submit --tag ...`).
2. Create Cloud SQL Postgres instance + db user.
3. Initialize the database with `odoo -i crm,sale_management,crm_lead_score --stop-after-init`.
4. `gcloud run deploy` with `--add-cloudsql-instances` and DB config via `--args`.

## License

LGPL-3 (same as Odoo Community).
