from odoo import models, fields, api

class BrandCustom(models.Model):
    _name = "brand.custom"
    _check_company_auto = True

    name = fields.Char(string="Brand Name", required=1)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)

    _sql_constraints = [
        ('unique_name_company', 'unique (name, company_id)', 'Name Must Be Unique !')
    ]