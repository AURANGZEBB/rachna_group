from odoo import fields, models

class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    print_format_id = fields.Many2one("ir.actions.report", string="Select Print Format")