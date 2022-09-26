from odoo import models, fields, _

class AccountMove(models.Model):
    _inherit = "account.move"

    batch_number = fields.Many2one("ta.batch", string="Batch Number")