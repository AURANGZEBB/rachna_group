from odoo import models, fields, api

class AccountPayment(models.Model):
    _inherit = "account.payment"

    lc_number = fields.Many2one("lc.import", string="LC #")
