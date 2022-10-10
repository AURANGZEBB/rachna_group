from odoo import fields, models,api,_
from odoo.tools import get_lang


class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_user_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    is_khi = fields.Boolean(string="Is KHI", related="x_user_id.is_khi")
    order_types_allowed = fields.Many2many("sale.order.type", related="x_user_id.order_types")

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_khi = fields.Boolean(string="Is KHI", related="order_id.is_khi")
    routes_allowed = fields.Many2many("stock.location.route", related="order_id.x_user_id.route_ids")
    type_id = fields.Many2one("sale.order.type", string="Type", related="order_id.type_id")


    @api.onchange('product_id')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        for line in self:
            line.price_unit = line.product_id.list_price * (
                            100 - line.order_id.partner_id.default_discount_percentage) / 100

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        res = super(SaleOrderLine, self).product_uom_change()
        for line in self:
            line.price_unit = line.product_id.list_price * (
                    100 - line.order_id.partner_id.default_discount_percentage) / 100