# -*- coding: utf-8 -*-
from odoo import api, fields, models

# Expected revenue (in company currency) at which a deal earns the full
# deal-size contribution. Anything above this is capped.
DEAL_SIZE_REFERENCE = 50000.0


class CrmLead(models.Model):
    # Extend the existing CRM model rather than create a new one.
    _inherit = "crm.lead"

    lead_score = fields.Integer(
        string="Lead Score",
        compute="_compute_lead_score",
        store=True,  # stored so it can be sorted, grouped and used in pivot/graph
        help="Automatic 0-100 score from win probability, deal size and contactability.",
    )
    score_band = fields.Selection(
        selection=[("hot", "Hot"), ("warm", "Warm"), ("cold", "Cold")],
        string="Score Band",
        compute="_compute_lead_score",
        store=True,
        help="Hot >= 70, Warm 40-69, Cold < 40.",
    )

    @api.depends("probability", "expected_revenue", "email_from", "phone")
    def _compute_lead_score(self):
        for lead in self:
            # 1. Win probability -> up to 40 points.
            prob_points = (lead.probability or 0.0) * 0.4

            # 2. Deal size -> up to 40 points, normalised against a reference deal.
            revenue = min(lead.expected_revenue or 0.0, DEAL_SIZE_REFERENCE)
            revenue_points = revenue / DEAL_SIZE_REFERENCE * 40.0

            # 3. Contactability -> up to 20 points.
            contact_points = (10.0 if lead.email_from else 0.0) + (10.0 if lead.phone else 0.0)

            score = int(round(prob_points + revenue_points + contact_points))
            lead.lead_score = max(0, min(100, score))

            if lead.lead_score >= 70:
                lead.score_band = "hot"
            elif lead.lead_score >= 40:
                lead.score_band = "warm"
            else:
                lead.score_band = "cold"
