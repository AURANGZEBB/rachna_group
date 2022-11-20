from odoo import models,fields,api

class SalePolicy(models.Model):
    _name = "sale.policy"

    name = fields.Char(string="Sequence", required=True, readonly=1)
    description = fields.Char(string="Policy Name", required=True)
    product_ids = fields.Many2many("product.template", string="Applicable on Products", required=True)
    policy_type = fields.Many2one("sale.policy.type", string="Sale Policy Type", required=True)
    exclude_policies = fields.Many2many("sale.policy", "relation_table_2221", "col_123","col_321", string="Excluded Policies")
    policy_line_ids = fields.One2many("sale.policy.line", "policy_id", string="Policy Line IDS")
    state = fields.Selection([
        ('draft', 'At The Time of Invoice'),
        ('confirm', 'PSI'),
        ('cancel', 'Cancelled'),
    ], string="Status", default="draft")

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_reset(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    _sql_constraints = [
        ('unique_name', 'unique (name)', 'Name Must Be Unique !')
    ]