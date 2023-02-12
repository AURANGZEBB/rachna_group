from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    policy_id = fields.Many2one("sale.policy", string="Policy")
    policy_total_advance = fields.Float(string="Policy Total Balance")
    policy_total_balance = fields.Float(string="Policy Total Balance")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    policy_id = fields.Many2one("sale.policy", string="Policy")
    policy_line_ids = fields.Many2many("sale.policy.line", string="Policy Line IDs")
    policy_line_balance = fields.Float(string="Policy Line Balance")