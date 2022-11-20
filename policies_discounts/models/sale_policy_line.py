from odoo import models,fields,api

class SalePolicyline(models.Model):
    _name = "sale.policy.line"

    name = fields.Char(string="name")
    description = fields.Char(string="Description")
    policy_id = fields.Many2one("sale.policy", string="Policy ID")
    parent_state = fields.Selection([
        ('draft', 'At The Time of Invoice'),
        ('confirm', 'PSI'),
        ('cancel', 'Cancelled'),
    ], string="Status", default="draft", related="policy_id.state", store=True)
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date From")
    benefit_id = fields.Many2one("sale.policy.benefit", string="Benefit")
    quantity = fields.Float(string="Quantity")
    value = fields.Float(string="Benefit Amount")
    total_value = fields.Float(string="Total", compute="compute_total_value", store=True)


    @api.onchange('benefit_id')
    def onchange_benefit(self):
        for rec in self:
            if rec.benefit_id:
                rec.quantity = rec.benefit_id.quantity
                rec.value = rec.benefit_id.value

    @api.depends('quantity', 'value')
    def compute_total_value(self):
        for rec in self:
            if not rec.quantity <= 0 and not rec.value <= 0:
                rec.total_value = rec.quantity * rec.value