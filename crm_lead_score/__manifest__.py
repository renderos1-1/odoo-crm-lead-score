# -*- coding: utf-8 -*-
{
    "name": "CRM Lead Score",
    "version": "17.0.1.0.0",
    "summary": "Automatic 0-100 lead score with Hot/Warm/Cold banding for CRM",
    "description": """
CRM Lead Score
==============
Adds an automatically-computed lead score (0-100) to every CRM lead/opportunity,
derived from three weighted signals:

* Win probability        -> up to 40 points
* Deal size (expected revenue, normalised to a reference deal) -> up to 40 points
* Contactability (email + phone present) -> up to 20 points

It also derives an analytics-friendly **Score Band** (Hot / Warm / Cold) so the
data can be grouped in pivot, graph and kanban views.
    """,
    "category": "Sales/CRM",
    "author": "Raxel Gerardo",
    "website": "https://example.com",
    "license": "LGPL-3",
    "depends": ["crm"],
    "data": [
        "views/crm_lead_views.xml",
    ],
    "application": False,
    "installable": True,
}
