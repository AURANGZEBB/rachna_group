from odoo import models, fields, _

class AccountMove(models.Model):
    _inherit = "account.move"

    courier_number = fields.Char(string="Courier Number")
    other_detail = fields.Char(string="Detail")
    batch_number = fields.Many2one("ta.batch", string="Batch Number")