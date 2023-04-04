# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

    policy_id = fields.Many2one("sale.policy", string="Policy", store=True)
    courier_number = fields.Char(string="Courier Number")
    previous_balance = fields.Float(string="Previous Balance")
    current_balance = fields.Float(string="Current Balance")

    def copy(self, default=None):
        invoices = super(AccountMove, self).copy()
        for i in invoices:
            i.invoice_line_ids = [(5,0,0)]
            
    def get_balance(self):
        for rec in self:
            balance_obj = rec.env['account.move.line'].search([('parent_state','in',['posted']),
                                                               ('account_internal_type', 'in', ['payable','receivable']),
                                                               ('partner_id', '=', self.partner_id.parent_id.id if self.partner_id.parent_id else self.partner_id.id),
                                                               ('move_id', '!=', self.id)])
            balance = sum(balance_obj.mapped('balance'))
            rec.previous_balance = round(balance, ndigits=2)
            rec.current_balance = round((balance + (-1 * rec.amount_total if rec.move_type in ['out_refund', 'in_invoice'] else rec.amount_total)),ndigits=2)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        rtn = super(AccountMove, self)._onchange_partner_id()
        self.get_balance()
        return rtn

    @api.onchange('amount_total')
    def _onchange_amount_total(self):
        for rec in self:
            rec.get_balance()

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    account_type = fields.Many2one("account.account.type", string="Account Type", related="account_id.user_type_id", store=True)
    product_category = fields.Many2one("product.category", string="Product Category", related="product_id.categ_id", store=True)
    policy_id = fields.Many2one("sale.policy", string="Policy")
    policy_line_ids = fields.Many2many("sale.policy.line", string="Policy Lines")
    policy_line_balance = fields.Float(string="Pol line Balance")
    sale_person_id = fields.Many2one("res.users", string="Sales Person ID", related="partner_id.user_id", store=True)
    sale_team_id = fields.Many2one("crm.team", string="Sales Team ID", related="partner_id.team_id", store=True)
    customer_rank = fields.Integer(string="Customer Rank", related="partner_id.customer_rank", store=True)
    tax_amount_tmp = fields.Float(string="Temporary Tax Amount **  Jugar")
    tax_line_amount = fields.Float(string="Tax Amount", related="tax_amount_tmp", store=True)

    @api.onchange('quantity', 'price_unit')
    def onchange_quantity(self):
        if self.policy_line_ids:
            if self.price_subtotal > self.policy_line_balance:
                raise ValidationError("Total Cannot be more that Balance Available !!!!")
            else:
                self.policy_line_ids = [(5,0,0)]
                self.policy_line_balance = ""
                self.discount = ""

    @api.onchange('tax_ids')
    def onchange_tax_ids(self):
        for rec in self:
            tax_amount = 0.0
        if rec.tax_ids:
            for t in rec.tax_ids:
                if t.amount_type == "percent":
                    tax = t.amount / 100 * rec.quantity * rec.price_unit
                    tax_amount += tax
                    rec.tax_amount_tmp = tax_amount
                elif t.amount_type == "division":
                    tax = t.amount / (t.amount + 100) * rec.quantity * rec.price_unit
                    tax_amount += tax
                    rec.tax_amount_tmp = tax_amount
        else:
            rec.tax_amount_tmp = 0



    @api.depends('product_id', 'quantity' ,'price_unit', 'discount')
    def get_detail(self):
        for rec in self:
            if rec.account_id.user_type_id.name == "Receivable" or "Payable":
                #print("/////////////////////////////////////////")
                x_detail = ""
                x_qty = ""
                x_amount = ""
                x_discount = ""
                jv = rec.search([('move_id', '=', rec.move_id.id),('account_id', '!=', rec.account_id.id)])
                for record in jv:
                    x_detail = x_detail + (record.product_id.name or "Payment") + "\n"
                    x_amount = x_amount + str(record.price_subtotal or 0.0) + "\n"
                    x_qty = x_qty + (str(record.quantity or 0.0) + "\n") if rec.price_subtotal else "0.0"
                    x_discount = ((record.price_unit * record.quantity * record.discount/100) or "0.0" + "\n") if record.discount else "0.0"
                    rec.x_detail = x_detail
                    rec.x_qty = x_qty
                    rec.x_amount = x_amount
                    rec.x_discount = x_discount

    x_detail = fields.Text(string="Detail", compute="get_detail", store=True)
    x_qty = fields.Text(string="Qty", compute="get_detail", store=True)
    x_amount = fields.Text(string="Amount", compute="get_detail", store=True)
    x_discount = fields.Text(string="Discount", compute="get_detail", store=True)

    @api.model
    def today_filter(self):
        return [('date', '=', fields.Date.today())]