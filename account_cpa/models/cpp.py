# -*- coding: utf-8 -*-
import datetime

from lxml import etree
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = "res.partner"

    advance_loan_account = fields.Many2one("account.account", string="Advance/Loan Account", required=True)

    def action_view_sale_order(self):
        return

class CounterParty(models.Model):
    _name = "counter.party"

    name = fields.Char(string="Name")
    date = fields.Date(string="Date", required=True, default=datetime.datetime.today())
    detail = fields.Char(string="Detail", required=True, store=True)
    payment_type = fields.Selection([
        ('receive', 'Receive'),
        ('pay', 'Pay'),
        ('transfer', 'Transfer'),
        ], string="Payment Type", help="Payment Type", required=True, default="")
    transaction_with = fields.Selection([
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ], string="Transaction With", help="Payment Type", required=True, store=True)
    counter_adj_type = fields.Selection([
        ('through_loan', 'Through Loan/Advance'),
        ('advance_cash_or_bank', 'Loan/Advance in Cash/Bank'),
        ('advance_against_policy', 'Advance Against Policy'),
        # ('transfer_advance_between_policy', 'Transfer Advance Between Policy'),
        ('advance_against_policy_through_loan', 'Advance Against Policy Through Loan'),
        ('return_advance_against_policy', 'Return Advance Against Policy'),
        ], string="Counter Party Adj. Type", help="Counter Adjustment Type", required=True, default="")

    policy_id = fields.Many2one("sale.policy", string="Policy")
    to_policy_id = fields.Many2one("sale.policy", string="To Policy")
    debit_policy = fields.Many2one("sale.policy", string="Debit Policy")
    credit_policy = fields.Many2one("sale.policy", string="Credit Policy")
    account_debit = fields.Many2one("account.account", string="Debit Account")
    account_credit = fields.Many2one("account.account", string="Credit Account")
    debit_partner = fields.Many2one("res.partner", string="Debit Partner")
    credit_partner = fields.Many2one("res.partner", string="Credit Partner")
    currency_id = fields.Many2one("res.currency", string="Currency")
    currency_amount = fields.Float(string="Amount in Currency")
    rate = fields.Float(string="Rate", required=True, default=1.0)
    amount = fields.Float(string="Amount", compute="cal_amount", store=True)

    @api.depends('currency_id', 'currency_amount', 'rate')
    def cal_amount(self):
        for rec in self:
            if rec.currency_id and rec.currency_amount and rec.rate:
                rec.amount = rec.rate * rec.currency_amount
            else:
                rec.amount

    state = fields.Selection([
            ('draft', 'Draft'),
            ('post', 'Posted'),
            ('cancel', 'Cancelled'),
            ], string="State", help="State", required=True, default="draft")
    advance_state = fields.Selection([
            ('pending', 'Pending'),
            ('cleared', 'Cleared'),
            ('cancel', 'Cancelled'),
            ('none', 'None'),
            ], string="Advance State", help="State", required=True, default="none")

    advance_status = fields.Selection([])
    move_id = fields.Many2one("account.move", copy=False)
    journal_id = fields.Many2one("account.journal")
    cash_bank_journals_ids = fields.Many2one("account.journal")

    @api.onchange('policy_id', 'to_policy_id')
    def onchange_policy(self):
        for rec in self:
            rec.onchangepartnerid()

    @api.onchange('counter_party')
    def onchange_counterparty(self):
        journals = self.env['account.journal']
        for rec in self:
            if rec.counter_party and not rec.counter_party.advance_loan_account:
                raise ValidationError("There is no Loan/Advance Account on Selected Customer/Vendors Form !!!!")
            if rec.payment_type == "receive":
                if rec.counter_adj_type == "through_loan":
                    counter_journal = journals.search([('name', '=', 'Counter Misc. Operations')])
                    rec.debit_partner = rec.counter_party.id
                    rec.account_debit = rec.counter_party.advance_loan_account.id
                    rec.journal_id = counter_journal

                elif rec.counter_adj_type == "advance_against_policy_through_loan":
                    counter_journal = journals.search([('name', '=', 'Counter Misc. Operations')])
                    rec.debit_partner = rec.counter_party.id
                    rec.account_debit = rec.counter_party.advance_loan_account.id
                    rec.journal_id = counter_journal

            elif rec.payment_type == "pay":
                if rec.counter_adj_type == "through_loan":
                    counter_journal = journals.search([('name', '=', 'Counter Misc. Operations')])
                    rec.credit_partner = rec.counter_party.id
                    rec.account_credit = rec.counter_party.advance_loan_account.id
                    rec.journal_id = counter_journal

    counter_party = fields.Many2one("res.partner", string="Counter Party")

    @api.onchange('cash_bank_journals_ids')
    def onchangejournalid(self):
        for rec in self:
            if rec.partner_id:
                rec.journal_id = rec.cash_bank_journals_ids.id
                if rec.transaction_with == "customer" and rec.payment_type == "receive":
                    rec.account_debit = rec.cash_bank_journals_ids.default_account_id.id
                elif rec.transaction_with == "customer" and rec.payment_type == "pay":
                    rec.account_credit = rec.cash_bank_journals_ids.default_account_id.id
                elif rec.transaction_with == "customer":
                    rec.account_debit = rec.cash_bank_journals_ids.default_account_id.id
                elif rec.transaction_with == "vendor":
                    rec.account_credit = rec.cash_bank_journals_ids.default_account_id.id

    @api.onchange('payment_type')
    def onchangepaymenttype(self):
        for rec in self:
            if rec.partner_id:
                rec.onchangepartnerid()
            if rec.counter_party:
                rec.onchange_counterparty()
            if rec.payment_type == "transfer" and rec.counter_adj_type != "transfer_advance_between_policy":
                rec.payment_type = ""
                raise ValidationError("You cannot select transfer !!!")

    @api.onchange('counter_adj_type')
    def onchangecounteradjtype(self):
        for rec in self:
            rec.partner_id = False
            rec.counter_party = False
            rec.cash_bank_journals_ids = False
            if rec.counter_adj_type == "advance_against_policy":
                rec.payment_type = "receive"
                if rec.transaction_with != "customer":
                    raise ValidationError("You cannot select this on vendor")
            elif rec.counter_adj_type == "return_advance_against_policy":
                rec.payment_type = "pay"
                if rec.transaction_with != "customer":
                    raise ValidationError("You cannot select this on vendor")
            elif rec.counter_adj_type == "transfer_advance_between_policy":
                rec.payment_type = "transfer"
                if rec.transaction_with != "customer":
                    raise ValidationError("You cannot select this on vendor")
            elif rec.payment_type == "transfer":
                rec.payment_type = ""
                if rec.transaction_with != "customer":
                    raise ValidationError("You cannot select this on vendor")

    @api.onchange('partner_id')
    def onchangepartnerid(self):
        for rec in self:
            if rec.partner_id and not rec.partner_id.advance_loan_account:
                raise ValidationError("There is no Loan/Advance Account on Selected Customer/Vendors Form !!!!")
            if rec.payment_type == "receive":
                if rec.counter_adj_type == "through_loan":
                    rec.credit_partner = rec.partner_id.id
                    if rec.transaction_with == 'customer':
                        rec.account_credit = rec.partner_id.property_account_receivable_id.id
                    elif rec.transaction_with == 'vendor':
                        rec.account_credit = rec.partner_id.property_account_payable_id.id

                elif rec.counter_adj_type == "advance_cash_or_bank":
                    if rec. transaction_with == 'customer':
                        rec.advance_state = "pending"
                        rec.credit_partner = rec.partner_id.id
                        rec.debit_partner = rec.partner_id.id
                        rec.account_credit = rec.partner_id.advance_loan_account.id

                elif rec.counter_adj_type == "advance_against_policy":
                    if rec.policy_id:
                        rec.credit_policy = rec.policy_id.id
                        rec.debit_policy = rec.policy_id.id
                    if rec.partner_id:
                        rec.credit_partner = rec.partner_id.id
                        rec.debit_partner = rec.partner_id.id
                        if rec.partner_id.property_account_receivable_id:
                            rec.account_credit = rec.partner_id.property_account_receivable_id.id
                        else:
                            raise ValidationError("Accounts are not selected on Partner Form !!!!")

                elif rec.counter_adj_type == "advance_against_policy_through_loan":
                    if rec.policy_id:
                        rec.credit_policy = rec.policy_id.id
                        rec.debit_policy = rec.policy_id.id
                    if rec.partner_id:
                        rec.credit_partner = rec.partner_id.id
                        if rec.partner_id.property_account_receivable_id:
                            rec.account_credit = rec.partner_id.property_account_receivable_id.id
                        else:
                            raise ValidationError("Accounts are not selected on Partner Form !!!!")



            elif rec.payment_type == "pay":
                if rec.counter_adj_type == "through_loan":
                    rec.debit_partner = rec.partner_id.id
                    if rec.transaction_with == 'customer':
                        rec.account_debit = rec.partner_id.property_account_receivable_id.id
                    elif rec.transaction_with == 'vendor':
                        rec.account_debit = rec.partner_id.property_account_payable_id.id

                elif rec.counter_adj_type == "advance_cash_or_bank":
                    rec.advance_state = "pending"
                    rec.debit_partner = rec.partner_id.id
                    rec.account_debit = rec.partner_id.advance_loan_account.id

                elif rec.counter_adj_type == "return_advance_against_policy":
                    if rec.policy_id:
                        rec.credit_policy = rec.policy_id.id
                        rec.debit_policy = rec.policy_id.id
                    if rec.partner_id:
                        rec.credit_partner = rec.partner_id.id
                        rec.debit_partner = rec.partner_id.id
                        if rec.partner_id.property_account_receivable_id:
                            rec.account_debit = rec.partner_id.property_account_receivable_id.id
                        else:
                            raise ValidationError("Accounts are not selected on Partner Form !!!!")

            elif rec.payment_type == "transfer":
                if rec.counter_adj_type == "transfer_advance_between_policy":
                    if rec.policy_id and rec.to_policy_id:
                        rec.credit_policy = rec.to_policy_id.id
                        rec.debit_policy = rec.policy_id.id
                    if rec.partner_id:
                        rec.credit_partner = rec.partner_id.id
                        rec.debit_partner = rec.partner_id.id
                        if rec.partner_id.property_account_receivable_id:
                            rec.account_debit = rec.partner_id.property_account_receivable_id.id
                            rec.account_credit = rec.partner_id.property_account_receivable_id.id
                        else:
                            raise ValidationError("Accounts are not selected on Partner Form !!!!")

    partner_id = fields.Many2one("res.partner", string="Customer/Vendor")

    def action_draft(self):
        for rec in self:
            if rec.move_id:
                rec.move_id.button_draft()
            rec.state = "draft"

    def action_cancel(self):
        for rec in self:
            if rec.move_id:
                rec.move_id.button_cancel()
            rec.state = "cancel"

    def clear_advance(self):
        for rec in self:
            if rec.state == "post" and rec.advance_state != "cleared":
                if rec.counter_adj_type == "advance_cash_or_bank":
                    rec.action_draft()
                    if rec.transaction_with == "customer":
                        rec.account_credit = rec.partner_id.property_account_receivable_id.id
                    elif rec.transaction_with == "vendor":
                        rec.account_debit = rec.partner_id.property_account_payable_id.id
                    if not rec.credit_partner:
                        rec.credit_partner = rec.partner_id.id
                    if not rec.debit_partner:
                        rec.debit_partner = rec.partner_id.id
                    rec.advance_state = "cleared"
                    rec.action_post()


    def action_post(self):
        move = {
            'name': self.name,
            'date': self.date or datetime.datetime.today(),
            'journal_id': self.journal_id.id,
            # 'company_id': uid.company_id,
            # 'type': 'entry',
            'state': 'draft',
            'ref': str(self.detail) + '- ' +" " + '- ' + 'Transferred',
            'line_ids': [
                        (0, 0, {
                            'name': self.name or self.detail,
                            'policy_id': self.debit_policy.id if self.debit_policy else "",
                            'partner_id': self.debit_partner.id,
                            'account_id': self.account_debit.id,
                            'debit': self.amount
                        }),
                         (0, 0, {
                             # 'name': self.name or self.detail,
                             'policy_id': self.credit_policy.id if self.credit_policy else "",
                             'partner_id': self.credit_partner.id,
                             'account_id': self.account_credit.id,
                             'credit': self.amount,
                         })]
        }
        if not self.move_id:
            move_id = self.env['account.move'].create(move)
            move_id.post()
        elif self.move_id:
            move_id = self.move_id
            move_id.line_ids = [(5, 0, 0)]
            move_id.write(move)
            move_id.post()

        self.state = "post"

        return self.write({'move_id': move_id.id})