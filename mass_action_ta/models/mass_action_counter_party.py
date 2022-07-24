
from odoo import models, fields, api

class CounterParty(models.Model):
    _inherit = "counter.party"

    def assign_seq_custom(self):
        for rec in self:
            if not rec.name and rec.state == "post":
                rec.name = rec.move_id.name

    def post_all_draft(self):
        for rec in self:
            rec.action_post()