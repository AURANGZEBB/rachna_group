from odoo import models,fields,api

class SalePolicyBenefit(models.Model):
    _name = "sale.policy.benefit"

    name = fields.Char(string="Benefit Name")
    quantity = fields.Float(string="Quantity")
    value = fields.Float(string="Benefit Amount")
    total_value = fields.Float(string="Total", compute="compute_total_value", store=True)
    type = fields.Selection([
        ('invoice', 'At The Time of Invoice'),
        ('psi', 'PSI'),
    ], string="Calc Type", help="Calc Type", default="", required=True)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)

    @api.depends('quantity', 'value')
    def compute_total_value(self):
        for rec in self:
            if not rec.quantity <= 0 and not rec.value <= 0:
                rec.total_value = rec.quantity * rec.value

    _sql_constraints = [
        ('unique_name_company', 'unique (name, company_id)', 'Name Must Be Unique !')
    ]