from odoo import models, fields, _

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    batch_number = fields.Many2one("ta.batch", string="Batch Number")
