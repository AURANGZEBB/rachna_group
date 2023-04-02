from odoo import models,fields,api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    policy_id = fields.Many2one("sale.policy", string="Policy")
    policy_total_advance = fields.Float(string="Policy Total Advance")
    policy_total_balance = fields.Float(string="Policy Total Balance")

    def copy(self, default=None):
        orders = super(SaleOrder, self).copy()
        for o in orders:
            o.order_line = [(5,0,0)]
        return orders


    @api.onchange('order_line')
    def func_order_lines(self):
        flag = 0
        previous_line = False
        for line in self.order_line:
            if not line.policy_line_ids and self.policy_id:
                flag = 1
                # line.policy_line_ids = [(5, 0, 0)]
                line.write({'policy_line_balance': 0,
                             'policy_line_ids': [(5, 0, 0)]})
                line.discount = ""
            elif flag == 1:
                line.policy_line_ids = [(5,0,0)]
                line.policy_line_balance = ""
                line.discount = ""

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['policy_id'] = self.policy_id.id if self.policy_id else ""
        print(invoice_vals)
        # print(self.abc)
        return invoice_vals

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    policy_id = fields.Many2one("sale.policy", string="Policy", related="order_id.policy_id")
    policy_line_ids = fields.Many2many("sale.policy.line", string="Policy Line IDs")
    policy_line_balance = fields.Float(string="Policy Line Balance")

    @api.onchange('policy_line_ids')
    def onchange_policy_line_ids(self):
        # self.onchange_price_unit()
        # self.order_id.func_order_lines()
        discount = 0.0
        line_balance_common = 0.0
        account_move_line_policy = self.env['account.move.line'].search([
                                                                        ('policy_id', '=', self.policy_id.id),
                                                                        ('parent_state', 'not in', ['cancel']),
                                                                        ('partner_id', '=', self.order_partner_id.id),
                                                                        ('account_type.type', 'in', ['receivable'])])
        invoices_and_creditnotes_lines = self.env['account.move.line'].search([
                                                                        ('policy_id', '=', self.policy_id.id),
                                                                        ('parent_state', 'not in', ['cancel']),
                                                                        ('partner_id', '=', self.order_partner_id.id),
                                                                        ('account_id.user_type_id.name', 'in', ['Income'])
                                                                    ])
        print(invoices_and_creditnotes_lines)
        for line in self.policy_line_ids:
            discount += line.benefit_id.value * 100
            self.discount = discount
            policy_line_advance = account_move_line_policy.filtered(lambda
                                                                        x: x.parent_state == 'posted' and x.date >= line.date_from and x.date <= line.date_to and not x.policy_line_ids and (
                        x.credit >= line.sale_slab_from or x.debit >= line.sale_slab_from) and (
                                                                                       x.credit <= line.sale_slab_to or x.debit <= line.sale_slab_to))
            invoices_lines = invoices_and_creditnotes_lines.filtered(lambda x: line.display_name in x.policy_line_ids.mapped('display_name')).mapped('credit')
            creditnotes_lines = invoices_and_creditnotes_lines.filtered(lambda x: line.display_name in x.policy_line_ids.mapped('display_name')).mapped('debit')
            previous_sale_order_lines_uninvoiced = self.search([('state', 'not in', ['cancel']),('id', '!=', self.order_id.order_line.ids),('policy_line_ids', 'in', line.ids),('invoice_status', 'not in', ['invoiced'])])
            current_sale_order_lines = self.order_id.order_line.filtered(lambda x: x != self) if not self.ids else self.order_id.order_line
            # print(current_sale_order_lines)
            total_sale_order_lines_uninvoiced = sum(previous_sale_order_lines_uninvoiced.mapped('price_subtotal')) + sum(current_sale_order_lines.mapped(lambda x: x.price_unit * x.product_uom_qty * (1 - discount / 100) if line in x.policy_line_ids else 0))
            print(total_sale_order_lines_uninvoiced, previous_sale_order_lines_uninvoiced, current_sale_order_lines)
            policy_line_advance_debit = sum(policy_line_advance.mapped('debit'))
            policy_line_advance_credit = sum(policy_line_advance.mapped('credit'))
            # print(policy_line_advance_debit, policy_line_advance_credit)
            net_total_policy_line_advance = policy_line_advance_credit - policy_line_advance_debit
            policy_line_invoices = sum(invoices_lines)
            policy_line_creditnotes = sum(creditnotes_lines)
            net_total_policy_line_invoices_and_creditnotes = policy_line_invoices - policy_line_creditnotes
            policy_line_balance = net_total_policy_line_advance - net_total_policy_line_invoices_and_creditnotes - total_sale_order_lines_uninvoiced
            line.policy_line_balance = policy_line_balance
            line_balance = policy_line_balance
            if line_balance == 0:
                raise ValidationError("Balance is not available for Policy --- "+ line.display_name)
            elif line_balance_common == 0.0:
                line_balance_common = line_balance
                self.policy_line_balance = line_balance
            elif line_balance_common != line_balance:
                raise ValidationError("Balance is Not same for Policy Line")

            # print(line_balance)
            print(self.price_subtotal)
            print(self.policy_line_balance)
            if self.price_subtotal > self.policy_line_balance and self.policy_line_ids:
                raise ValidationError("Total Cannot be more than Balance Available !!!!")

    @api.onchange('price_unit', 'product_uom_qty')
    def onchange_price_unit(self):
        if self.policy_line_ids:
            if self.price_subtotal > self.policy_line_balance:
                raise ValidationError("Total Cannot be more that Balance Available !!!!")
            else:
                self.policy_line_ids = [(5,0,0)]
                self.policy_line_balance = ""
                self.discount = ""

    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        :param optional_values: any parameter that should be added to the returned invoice line
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
            'policy_id': self.policy_id.id if self.policy_id else "",
            'policy_line_ids': self.policy_line_ids,
            'policy_line_balance': self.policy_line_balance,
        }
        if self.order_id.analytic_account_id and not self.display_type:
            res['analytic_account_id'] = self.order_id.analytic_account_id.id
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res