import datetime

from odoo import api, fields, models, _


class DynamicReportLedger(models.TransientModel):
    _name = "dynamic.report.ledger"

    @api.model
    def ta_get_dynamic_report_values(self, type=0, partner_id=0, date_start=False, date_end=False):
        if type == 1:
            data = self.ta_get_report_values(partner_id, date_start, date_end)
            return data

    @api.model
    def ta_get_report_values(self, partner_id=False, date_start=False, date_end=False):
        data = None
        company_id = self.env.company
        if partner_id and partner_id != "None":
            partner = self.env['res.partner'].search([('id', '=', int(partner_id))])
            opening_balance = 0
            opening_debit_sum = 0
            opening_credit_sum = 0
            if date_start and date_end:
                opening_moves_lines = self.env['account.move.line'].search([('company_id', '=', company_id.id),
                                                                            ('parent_state', '=', 'posted'),
                                                                            ('partner_id', '=', partner.id),
                                                                            ('date', '<', date_start),
                                                                            '|',('account_type.name', '=', 'Receivable'),('account_type.name', '=', 'Payable')
                                                                            ])

                opening_debit_sum = sum(opening_moves_lines.mapped('debit'))
                opening_credit_sum = sum(opening_moves_lines.mapped('credit'))
                opening_balance = opening_debit_sum - opening_credit_sum
                all_posted_moves_lines = self.env['account.move.line'].search([('company_id', '=', company_id.id),
                                                                               ('partner_id', '=', partner.id),
                                                                               ('date', '>=', date_start),
                                                                               ('date', '<=', date_end),
                                                                               ('parent_state', '=', 'posted'),
                                                                               '|',
                                                                               ('account_type.name', '=', 'Income'),
                                                                               ('account_type.name', '=', 'Receivable'),
                                                                               ],order="date asc")
            else:
                all_posted_moves_lines = self.env['account.move.line'].search([('company_id', '=', company_id.id),
                                                                               ('partner_id', '=', partner.id),
                                                                               ('parent_state', '=', 'posted'),
                                                                               '|', ('account_type.name', '=', 'Income'), ('account_type.name', '=', 'Receivable')], order="date asc")
            lines_data = []
            net_balance = opening_balance
            total_debit = 0.0
            total_credit = 0.0
            for line in all_posted_moves_lines:
                if line.journal_id.type in ["sale", "purchase"] and line.account_id.user_type_id.name == ("Receivable" or "Payable"):
                    pass
                else:
                    amount = line.amount_currency * -1 if line.journal_id.type in ["sale","purchase"] else line.amount_currency
                    debit = amount if amount > 0 else 0
                    credit = amount * -1 if amount < 0 else 0
                    total_debit += debit
                    total_credit += credit
                    net_balance += amount
                    lines_data.append({
                                    'id': line.move_id.id,
                                    'date': line.date,
                                    'product': line.product_id.name if line.product_id else "",
                                    'name': line.move_id.name,
                                    'quantity': line.quantity if line.quantity else "",
                                    'uom': line.product_uom_id.name if line.product_id else "",
                                    'description': line.ref if line.ref else line.name if line.name else "",
                                    'policy': line.policy_id.name if line.policy_id else "",
                                    'price_unit': line.price_unit if line.price_unit else "",
                                    'amount': amount,
                                    'debit': debit,
                                    'credit': credit,
                                    'net_balance': round(net_balance,2),
                                })

            data = {
                    'date_start': date_start,
                    'date_end': date_end,
                    'company_name': self.env.company.name,
                    'partner_name': partner.name,
                    'partner_address': partner.street if partner.street else "" + ", " + partner.city if partner.city else "" + ", " + partner.state_id.name if partner.state_id else "" + ", " + partner.country_id.name if  partner.country_id else "",
                    'partner_phone': partner.phone if partner.phone else "" + ", " + partner.mobile if partner.mobile else "",
                    'sales_team': partner.team_id.name if partner.team_id else "",
                    'sales_person': partner.user_id.name if partner.user_id else "",
                    'payment_terms': partner.property_payment_term_id.name if partner.property_payment_term_id else "",
                    'opening_debit': opening_debit_sum,
                    'opening_credit': opening_credit_sum,
                    'opening_balance': opening_balance,
                    'total_debit': total_debit + opening_debit_sum,
                    'total_credit': total_credit + opening_credit_sum,
                    'closing_balance': round(net_balance,2),
                    'lines_data': lines_data,
                    }
        # print("//////////////////////////", data)

        return data

    @api.model
    def ta_get_report_filters(self, type=0):
        if type == 1:
            filters = self.ta_filter()
            # print(filters)
            return filters

    @api.model
    def ta_filter(self):
        partners = self.env['res.partner'].search_read([('customer_rank', '>', 0)],['id', 'name'])

        filters = {'partners' : partners}

        return filters