from odoo import models,fields,api

class SalePolicyline(models.Model):
    _name = "sale.policy.line"

    name = fields.Char(string="name")
    description = fields.Char(string="Description")
    policy_id = fields.Many2one("sale.policy", string="Policy ID")

    parent_state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Running'),
        ('close', 'Closed'),
        ('cancel', 'Cancelled'),
    ], string="Status", default="draft", related="policy_id.state", store=True)
    calc_type = fields.Selection([('invoice', 'At The Time of Invoice'), ('psi', 'PSI')], string="Calc Type",
                                 related="policy_id.calc_type")

    sale_slab_from = fields.Float(string="Sale Slab From") # for PSI only
    sale_slab_to = fields.Float(string="Sale Slab To") # for PSI only
    applicable_date_from = fields.Date(string="Applicable Date From", related="policy_id.applicable_date_from")  # For PSI Policy Only
    applicable_date_to = fields.Date(string="Applicable Date to", related="policy_id.applicable_date_to")  # For PSI Policy Only
    date_from = fields.Date(string="Date From") # for policy at the time of invoice only
    date_to = fields.Date(string="Date To") # for policy at the time of invoice only
    benefit_id = fields.Many2one("sale.policy.benefit", string="Benefit")
    quantity = fields.Float(string="Quantity")
    value = fields.Float(string="Benefit Amount")
    total_value = fields.Float(string="Total", compute="compute_total_value", store=True)
    company_id = fields.Many2one("res.company", string="Company", related="policy_id.company_id")
    total_advance_against_line = fields.Float(string="Line Advance", readonly=1)
    policy_line_balance = fields.Float(string="Line Balance", readonly=1)

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