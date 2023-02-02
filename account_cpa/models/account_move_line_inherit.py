# -*- coding: utf-8 -*-
import datetime

from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    policy_id = fields.Many2one("sale.policy", string="Policy")

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    account_type = fields.Many2one("account.account.type", string="Account Type", related="account_id.user_type_id", store=True)
    product_category = fields.Many2one("product.category", string="Product Category", related="product_id.categ_id", store=True)
    policy_id = fields.Many2one("sale.policy", string="Policy")
    policy_line_ids = fields.Many2many("sale.policy.line", string="Policy Lines")
    sales_person_id = fields.Many2one("res.users", related="move_id.invoice_user_id", store=True)
    sales_team_id = fields.Many2one("crm.team", related="move_id.team_id", store=True)

    def get_sales_person_on_payment(self):
        for rec in self:
            if rec.move_id.payment_id and rec.move_id.journal_id.type == "cash" or rec.move_id.journal_id.type == "bank":
                if rec.move_id.payment_id.reconciled_invoice_ids:
                    var_salesperson = rec.move_id.payment_id.reconciled_invoice_ids[0].invoice_user_id.id
                    var_salesteam = rec.move_id.payment_id.reconciled_invoice_ids[0].team_id
                    rec.move_id.invoice_user_id = var_salesperson
                    rec.move_id.team_id = var_salesteam.id if var_salesteam else ""
                    print(var_salesperson,"---", rec.move_id.invoice_user_id)
                    rec.eval_function = None
                    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            else:
                rec.eval_function = None
                print("elseesleeslelselseleslselseleslselsel")

    eval_function = fields.Char(string="Sales Person ID Custom", compute="get_sales_person_on_payment")

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