from odoo import api, fields, models, _


class DynamicReportLedger(models.TransientModel):
    _name = "dynamic.report.ledger"

    @api.model
    def ta_get_dynamic_report_values(self, type=0, partner_id=0):
        if type == 1:
            data = self.ta_get_report_values(partner_id)
            return data
    @api.model
    def ta_get_report_values(self, partner_id=False):
        data = None
        company_id = self.env.company
        # Type 1
        # print("---------", partner_id)
        if partner_id and partner_id != "None":
            partner = self.env['res.partner'].search([('id', '=', int(partner_id))])
            all_moves = self.env['account.move']
            invoices = all_moves.search([('company_id', '=', company_id.id),('partner_id', '=', int(partner_id)),('state', 'in', ['posted']),('move_type', 'in', ['out_invoice'])])
            invoices_total = sum(invoices.mapped('amount_total'))
            credit_notes = all_moves.search([('company_id', '=', company_id.id),('partner_id', '=', int(partner_id)),('state', '=', 'posted'),('move_type', '=', 'out_refund')])
            credit_notes_total = sum(credit_notes.mapped('amount_total'))
            bills = all_moves.search([('company_id', '=', company_id.id),('partner_id', '=', int(partner_id)),('state', '=', 'posted'),('move_type', '=', 'in_invoice')])
            debit_notes = all_moves.search([('company_id', '=', company_id.id),('partner_id', '=', int(partner_id)),('state', '=', 'posted'),('move_type', '=', 'in_refund')])
            payments_or_other_entries = self.env['account.move.line'].search(
                [('company_id', '=', company_id.id), ('partner_id', '=', int(partner_id)), ('parent_state', '=', 'posted'), ('journal_id.name', '!=', 'Customer Invoices' or 'Vendor Bills'), ('account_type.type', 'in', ['receivable'])])
            data_payments_or_other_entries = []
            payments_or_other_entries_debit = sum(payments_or_other_entries.mapped('debit'))
            payments_or_other_entries_credit = sum(payments_or_other_entries.mapped('credit'))
            net_total_payments_or_other_entries = payments_or_other_entries_debit - payments_or_other_entries_credit
            invoices_data = []
            credit_notes_data = []
            #  Below code is for Invoices
            for i in invoices:
                invoice_lines = []
                for line in i.invoice_line_ids:
                    invoice_lines.append({
                        'product': line.product_id.name,
                        'name': line.name,
                        'quantity': line.quantity,
                        'uom': line.product_uom_id.name,
                        'price_unit': line.price_unit,
                        'price_subtotal': line.price_subtotal,
                    })
                data = {
                    'id': i.id,
                    'number': i.name,
                    'partner': i.partner_id.name,
                    'invoice_date': i.invoice_date,
                    'amount_total': i.amount_total,
                    'invoice_lines': invoice_lines,
                }
                invoices_data.append(data)
            # Below code is for Credit Notes
            for c in credit_notes:
                credit_notes_lines = []
                for line in c.invoice_line_ids:
                    credit_notes_lines.append({
                        'product': line.product_id.name,
                        'name': line.name,
                        'quantity': line.quantity,
                        'uom': line.product_uom_id.name,
                        'price_unit': line.price_unit,
                        'price_subtotal': line.price_subtotal * -1 if line.price_subtotal else line.price_subtotal,
                    })
                data = {
                    'id': c.id,
                    'number': c.name,
                    'partner': c.partner_id.name,
                    'invoice_date': c.invoice_date,
                    'amount_total': c.amount_total * -1 if c.amount_total else c.amount_total,
                    'invoice_lines': credit_notes_lines,
                }
                credit_notes_data.append(data)
            # Below code is for payments or other entries
            for p in payments_or_other_entries:
                data = {
                    'move_date': p.date,
                    'move_id': p.move_id,
                    'move_name': p.move_id.name,
                    'account_id': p.account_id.name,
                    'ref': p.ref,
                    'name': p.name,
                    'amount': p.debit - p.credit,
                }
                data_payments_or_other_entries.append(data)
            data = {
                    'company_name': self.env.company.name,
                    'partner_name': partner.name,
                    'invoices_data': invoices_data,
                    'len_invoices_data': len(invoices_data),
                    'invoices_total': invoices_total,
                    'credit_notes_total': credit_notes_total * -1 if credit_notes_total else 0,
                    'credit_notes_data': credit_notes_data,
                    'len_credit_notes_data': len(credit_notes_data),
                    'data_payments_or_other_entries': data_payments_or_other_entries,
                    'len_data_payments_or_other_entries': len(data_payments_or_other_entries),
                    'net_total_payments_or_other_entries': net_total_payments_or_other_entries,
                    'net_balance': round(invoices_total - credit_notes_total + net_total_payments_or_other_entries,2),
                    }

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