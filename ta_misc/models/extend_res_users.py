from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    is_khi = fields.Boolean("Is KHI")
    route_ids = fields.Many2many("stock.location.route", string="Route IDS Allowed")
    operation_type_ids = fields.Many2many("stock.picking.type", string="Operation Types Allowed")
    journal_ids = fields.Many2many("account.journal", string="Journals")
    order_types = fields.Many2many("sale.order.type", string="Order Types")
    initials = fields.Char(string="Initials", required=True)
