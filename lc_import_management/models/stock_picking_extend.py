from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    lc_number = fields.Many2one("lc.import", string="LC #")
