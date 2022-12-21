from odoo import models

class TaxReportXlsx(models.AbstractModel):
    _name = 'report.report_multi.tax_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        account_move_invoice = self.env['account.move'].search([('invoice_date', '>=', data['date_from']),
                                                           ('invoice_date', '<=', data['date_to']),
                                                           ('move_type', 'in', ['out_invoice']),
                                                           ('state', 'in', ['posted']),
                                                           ('amount_tax', '>', 0),
                                                         ])
        account_move_credit_note = self.env['account.move'].search([('date', '>=', data['date_from']),
                                                            ('date', '<=', data['date_to']),
                                                            ('move_type', 'in', ['out_refund']),
                                                            ('state', 'in', ['posted']),
                                                            ('amount_tax', '>', 0),
                                                         ])
        H1 = workbook.add_format({'font_size': 28, 'align': 'center', 'bold': True})
        H3 = workbook.add_format({'font_size': 14, 'align': 'center', 'bold': True})
        H4 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True, 'text_wrap': True})
        H5 = workbook.add_format({'font_size': 10, 'align': 'center'})
        date_format = workbook.add_format({'num_format': 'dd/mm/yy'})
        date_format2 = workbook.add_format({'font_size': 14, 'num_format': 'dd/mm/yy'})
        sheet_inv = workbook.add_worksheet('Tax Report')
        sheet_credit_note = workbook.add_worksheet('Tax Credit Note Report')

        #################### Headings  Inv ##############################
        sheet_inv.write(6, 0, "Date", H4)
        sheet_inv.write(6, 1, "Invoice#", H4)
        sheet_inv.write(6, 2, "Customer", H4)
        sheet_inv.write(6, 3, "VAT", H4)
        sheet_inv.write(6, 4, "NTN", H4)
        sheet_inv.write(6, 5, "CNIC", H4)
        sheet_inv.write(6, 6, "HS Code", H4)
        sheet_inv.write(6, 7, "Journal", H4)
        sheet_inv.write(6, 8, "Tax@17%", H4)
        sheet_inv.write(6, 9, "Invoice Total", H4)
        # ##################################/////////////////////#####################################
        row = 7
        for rec in account_move_invoice:
            sheet_inv.write(row, 0, rec.invoice_date, date_format)
            sheet_inv.write(row, 1, rec.name)
            sheet_inv.write(row, 2, rec.partner_id.name)
            sheet_inv.write(row, 3, rec.partner_id.vat)
            sheet_inv.write(row, 4, rec.partner_id.ntn)
            sheet_inv.write(row, 5, rec.partner_id.cnic)
            sheet_inv.write(row, 6, rec.invoice_line_ids[0].x_hscode if rec.invoice_line_ids else "-")
            sheet_inv.write(row, 7, rec.journal_id.name)
            sheet_inv.write(row, 8, rec.amount_tax)
            sheet_inv.write(row, 9, rec.amount_total)

        ##########Adjusting column width######################
        sheet_inv.set_column(6, 0, 20)
        sheet_inv.set_column(6, 1, 12)

        # sheet.insert_image('A1', r'/opt/odoo13/custom_addons/ta_hrm/static/images/logo.png', {'x_scale': 0.5, 'y_scale': 0.5})
        sheet_inv.write(1, 5, "Tax Report", H1)
        sheet_inv.write(3, 3, "From:", H3)
        sheet_inv.write(3, 5, "To:", H3)
        sheet_inv.write(3, 4, data['date_from'], date_format2)
        sheet_inv.write(3, 6, data['date_to'], date_format2)
        # ________________________________________________________________________________

        # #############################  Credit Note ###############################################
        #################### Headings  Inv ##############################
        sheet_credit_note.write(6, 0, "Date", H4)
        sheet_credit_note.write(6, 1, "Credit Note#", H4)
        sheet_credit_note.write(6, 2, "Customer", H4)
        sheet_credit_note.write(6, 3, "VAT", H4)
        sheet_credit_note.write(6, 4, "NTN", H4)
        sheet_credit_note.write(6, 5, "CNIC", H4)
        sheet_credit_note.write(6, 6, "HS Code", H4)
        sheet_credit_note.write(6, 7, "Journal", H4)
        sheet_credit_note.write(6, 8, "Tax@17%", H4)
        sheet_credit_note.write(6, 9, "Invoice Total", H4)
        # ##################################/////////////////////#####################################
        row = 7
        for rec in account_move_credit_note:
            sheet_credit_note.write(row, 0, rec.invoice_date, date_format)
            sheet_credit_note.write(row, 1, rec.name)
            sheet_credit_note.write(row, 2, rec.partner_id.name)
            sheet_credit_note.write(row, 3, rec.partner_id.vat)
            sheet_credit_note.write(row, 4, rec.partner_id.ntn)
            sheet_credit_note(row, 5, rec.partner_id.cnic)
            sheet_credit_note.write(row, 6, rec.invoice_line_ids[0].product_id.x_hscode if rec.invoice_line_ids else "-")
            sheet_credit_note.write(row, 7, rec.journal_id.name)
            sheet_credit_note.write(row, 8, rec.amount_tax)
            sheet_credit_note.write(row, 9, rec.amount_total)

        ##########Adjusting column width######################
        sheet_credit_note.set_column(6, 0, 20)
        sheet_credit_note.set_column(6, 1, 12)

        # sheet.insert_image('A1', r'/opt/odoo13/custom_addons/ta_hrm/static/images/logo.png', {'x_scale': 0.5, 'y_scale': 0.5})
        sheet_credit_note.write(1, 5, "Tax Credit Note Report", H1)
        sheet_credit_note.write(3, 3, "From:", H3)
        sheet_credit_note.write(3, 5, "To:", H3)
        sheet_credit_note.write(3, 4, data['date_from'], date_format2)
        sheet_credit_note.write(3, 6, data['date_to'], date_format2)
        # ________________________________________________________________________________
