from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    lc_number = fields.Many2one("lc.import", string="LC #")