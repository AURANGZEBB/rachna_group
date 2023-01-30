from odoo import models, fields, api

class LcImport(models.Model):
    _name = "lc.import"

    name = fields.Char(string="LC #", required=1)
    description = fields.Char(string="Description", required=1)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)

    _sql_constraints = [
        ('unique_name_per_company', 'unique (name,company_id)', 'Name Must Be Unique !')
    ]