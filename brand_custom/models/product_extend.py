from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    brand = fields.Many2one("brand.custom", string="Brand")