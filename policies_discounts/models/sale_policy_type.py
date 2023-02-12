from odoo import models,fields,api

class SalePolicyType(models.Model):
    _name = "sale.policy.type"
    _check_company_auto = True

    name = fields.Char(string="Policy Type", required=True)
    description = fields.Char(string="Description")
    calc_type = fields.Selection([
        ('invoice', 'At The Time of Invoice'),
        ('psi', 'PSI'),
    ], string="Calc Type", help="Calc Type", default="", required=True)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)

    _sql_constraints = [
        ('unique_name_company', 'unique (name, company_id)', 'Name Must Be Unique !')
    ]