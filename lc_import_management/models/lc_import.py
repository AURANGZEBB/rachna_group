from odoo import models, fields, api

class LcImport(models.Model):
    _name = "lc.import"

    name = fields.Char(string="LC #", required=1)
    description = fields.Char(string="Description", required=1)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)
    purchase_order_ids = fields.One2many('purchase.order', 'lc_number', string="Purchase Orders")
    account_move_ids = fields.One2many('account.move', 'lc_number', string="Bills")
    account_payment_ids = fields.One2many('account.payment', 'lc_number', string="Payments")

    _sql_constraints = [
        ('unique_name_per_company', 'unique (name,company_id)', 'Name Must Be Unique !')
    ]