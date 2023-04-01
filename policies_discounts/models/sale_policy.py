from odoo import models,fields,api, _
from odoo.exceptions import ValidationError

class SalePolicy(models.Model):
    _name = "sale.policy"
    _check_company_auto = True

    name = fields.Char(string="Sequence", readonly=1)
    applicable_date_from = fields.Date(string="Applicable Date From") # For PSI Policy Only
    applicable_date_to = fields.Date(string="Applicable Date to") # For PSI Policy Only
    description = fields.Char(string="Policy Name", required=True)
    product_ids = fields.Many2many("product.template", string="Applicable on Products", required=True)
    policy_type = fields.Many2one("sale.policy.type", string="Sale Policy Type", required=True)
    calc_type = fields.Selection([('invoice', 'At The Time of Invoice'), ('psi', 'PSI')], string="Calc Type", related="policy_type.calc_type")
    exclude_policies = fields.Many2many("sale.policy", "relation_table_2221", "col_123","col_321", string="Excluded Policies")
    policy_line_ids = fields.One2many("sale.policy.line", "policy_id", string="Policy Line IDS")
    slab_applicable = fields.Boolean(string="Slab Applicable")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Running'),
        ('close', 'Closed'),
        ('cancel', 'Cancelled'),
    ], string="Status", default="draft")
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)
    policy_total_advance = fields.Float(string="Total Advance Against Policy")

    def clear_product_ids(self):
        if self.state == 'draft':
            self.product_ids = False
        else:
            raise ValidationError("State Not in Draft !!!!!")

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_reset(self):
        for rec in self:
            rec.state = 'draft'

    def action_close(self):
        for rec in self:
            rec.state = 'close'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


    def get_policy_advance(self):
        for rec in self:
            account_move_line_policy = rec.env['account.move.line'].search([
                                                                            ('policy_id', '=', rec.id),
                                                                            ('parent_state', 'not in', ['cancel']),
                                                                            ('account_type.type', 'in', ['receivable'])])
            sale_order_lines_uninvoiced = rec.env['sale.order.line'].search([('state', 'not in', ['cancel'])])
            debit_list = account_move_line_policy.mapped('debit') # Return of Advance
            credit_list = account_move_line_policy.mapped('credit') # Credit means advance collected

            total_advance = sum(credit_list)
            rec.policy_total_advance = total_advance

            for line in rec.policy_line_ids:
                policy_line_advance = account_move_line_policy.filtered(lambda x: x.parent_state in 'posted' and x.date >= line.date_from and x.date <= line.date_to and not x.policy_line_ids and (x.credit >= line.sale_slab_from or x.debit >= line.sale_slab_from) and (x.credit <= line.sale_slab_to or x.debit <= line.sale_slab_to))
                invoices_and_creditnotes_lines = account_move_line_policy.filtered(lambda x: x.policy_line_ids and x.policy_line_ids in line.ids)
                sale_order_lines_uninvoiced_policy_lines = sale_order_lines_uninvoiced.filtered(lambda x: x.policy_line_ids and line.id in x.policy_line_ids.ids)
                total_sale_order_lines_uninvoiced = sum(sale_order_lines_uninvoiced_policy_lines.mapped('price_subtotal'))
                policy_line_advance_debit = sum(policy_line_advance.mapped('debit'))
                policy_line_advance_credit = sum(policy_line_advance.mapped('credit'))
                # print(policy_line_advance_debit, policy_line_advance_credit)
                net_total_policy_line_advance = policy_line_advance_credit - policy_line_advance_debit
                policy_line_invoices = sum(invoices_and_creditnotes_lines.mapped('debit'))
                policy_line_creditnotes = sum(invoices_and_creditnotes_lines.mapped('credit'))
                net_total_policy_line_invoices_and_creditnotes = policy_line_invoices - policy_line_creditnotes
                policy_line_balance = net_total_policy_line_advance + net_total_policy_line_invoices_and_creditnotes - total_sale_order_lines_uninvoiced
                line.policy_line_balance = policy_line_balance

            vals = {
                'debit_list': debit_list,
                'credit_list': credit_list,
                'gross_total_advance': sum(credit_list),
                'net_balance_advance': sum(credit_list) - sum(debit_list),
            }


            # print(account_move_line_policy, debit_list, credit_list)

            return vals

    def name_get(self):
        result = []
        for rec in self:
            name = rec.name + '-' + rec.description
            result.append((rec.id, name))
        return result

    @api.model
    def create(self, vals_list):
        vals_list['name'] = self.env['ir.sequence'].next_by_code('sequence.sale.policy') or _('New')
        rtn = super(SalePolicy, self).create(vals_list)
        return rtn

    _sql_constraints = [
        ('unique_name_company', 'unique (name, company_id)', 'Name Must Be Unique !')
    ]
