from odoo import models,fields,api

class SalePolicyType(models.Model):
    _name = "sale.policy.type"

    name = fields.Char(string="Policy Type", required=True)
    description = fields.Char(string="Description")
    calc_type = fields.Selection([
        ('invoice', 'At The Time of Invoice'),
        ('psi', 'PSI'),
    ], string="Calc Type", help="Calc Type", default="", required=True)

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Name Must Be Unique !')
    ]