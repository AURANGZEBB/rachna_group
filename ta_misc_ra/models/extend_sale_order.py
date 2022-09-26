from odoo import models, fields, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    batch_number = fields.Many2one("ta.batch", string="Batch Number")