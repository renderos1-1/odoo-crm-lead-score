# Odoo 17 with our custom CRM Lead Score module baked in.
# /mnt/extra-addons is already on the addons_path in the official image.
FROM odoo:17

COPY crm_lead_score /mnt/extra-addons/crm_lead_score
