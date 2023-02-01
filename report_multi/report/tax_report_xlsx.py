from odoo import models

class TaxReportXlsx(models.AbstractModel):
    _name = 'report.report_multi.tax_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        account_move_invoice = self.env['account.move'].search([('invoice_date', '>=', data['date_from']),
                                                           ('invoice_date', '<=', data['date_to']),
                                                           ('move_type', 'in', ['out_invoice']),
                                                           ('state', 'in', ['posted']),
                                                           ('sale_type_id.tax_applies', '=', True),
                                                         ])
        account_move_credit_note = self.env['account.move'].search([('date', '>=', data['date_from']),
                                                            ('date', '<=', data['date_to']),
                                                            ('move_type', 'in', ['out_refund']),
                                                            ('state', 'in', ['posted']),
                                                            ('sale_type_id.tax_applies', '=', True),
                                                         ])
        H1 = workbook.add_format({'font_size': 28, 'align': 'center', 'bold': True})
        H3 = workbook.add_format({'font_size': 14, 'align': 'center', 'bold': True})
        H4 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': True, 'text_wrap': True})
        H5 = workbook.add_format({'font_size': 10, 'align': 'left'})
        H5_float = workbook.add_format({'font_size': 10, 'align': 'left', 'num_format': '0.00'})
        H5_percentage = workbook.add_format({'font_size': 10, 'align': 'left', 'num_format': '0.00%'})
        date_format = workbook.add_format({'num_format': 'dd-mmm-yy'})
        date_format2 = workbook.add_format({'font_size': 14, 'num_format': 'dd/mm/yy'})
        sheet_inv = workbook.add_worksheet('Tax Report')
        sheet_credit_note = workbook.add_worksheet('Tax Credit Note Report')

        #################### Headings  Inv ##############################
        sheet_inv.write(6, 0, "Sr.", H4)
        sheet_inv.write(6, 1, "Buyer NTN", H4)
        sheet_inv.write(6, 2, "Buyer Name", H4)
        sheet_inv.write(6, 3, "Buyer Type", H4)
        sheet_inv.write(6, 4, "Sale Origination Province of Supplier", H4)
        sheet_inv.write(6, 5, "Destination Province", H4)
        sheet_inv.write(6, 6, "Document Type", H4)
        sheet_inv.write(6, 7, "Document Number", H4)
        sheet_inv.write(6, 8, "Document Date", H4)
        sheet_inv.write(6, 9, "HS Code", H4)
        sheet_inv.write(6, 10, "Sale Type", H4)
        sheet_inv.write(6, 11, "Rate", H4) # Tax Rate
        sheet_inv.write(6, 13, "Quantity", H4) # Total Invoice Quantity
        sheet_inv.write(6, 14, "UOM", H4)
        sheet_inv.write(6, 15, "Value of Sales Excluding Sales Tax", H4)
        sheet_inv.write(6, 16, "Sales Tax", H4)
        sheet_inv.write(6, 17, "Fixed Value or Retail Price", H4)
        sheet_inv.write(6, 18, "Extra Tax", H4)
        sheet_inv.write(6, 19, "Further Tax", H4)
        sheet_inv.write(6, 20, "Total Value of Sales", H4)
        sheet_inv.write(6, 21, "ST Withheld at Source", H4)
        sheet_inv.write(6, 22, "SRO No. / Schedule No. ", H4)
        sheet_inv.write(6, 23, "Item S.No.", H4)
        # ##################################/////////////////////#####################################
        row = 7
        sr_number = 0
        for rec in account_move_invoice:
            sr_number += 1
            sheet_inv.write(row, 0, sr_number, H5)
            sheet_inv.write(row, 1, rec.partner_id.ntn if rec.partner_id.ntn else rec.partner_id.cnic if rec.partner_id.cnic else "-", H5)
            sheet_inv.write(row, 2, rec.partner_id.name, H5)
            sheet_inv.write(row, 4, "PUNJAB", H5)
            sheet_inv.write(row, 5, rec.partner_id.state_id.name if rec.partner_id.state_id else "-", H5)
            sheet_inv.write(row, 6, "Sale Invoice", H5)
            sheet_inv.write(row, 7, rec.name, H5)
            sheet_inv.write(row, 8, rec.invoice_date, date_format)
            # get max hs code amount line
            list_line_amount = []
            max_hscode = ""
            for line in rec.invoice_line_ids:
                list_line_amount.append(line.price_subtotal)
                if max(list_line_amount) == line.price_subtotal:
                    max_hscode = line.product_id.x_hscode_description
            sheet_inv.write(row, 9, max_hscode, H5)
            sheet_inv.write(row, 10, "Goods at standard rate (default)" if rec.amount_tax else "Exempt goods", H5)
            if rec.amount_tax:
                sheet_inv.write(row, 11, 0.17, H5_percentage)
            else:
                sheet_inv.write(row, 11, "Exempt", H5)
            sheet_inv.write(row, 13, sum(rec.invoice_line_ids.mapped('quantity')), H5_float)
            sheet_inv.write(row, 14, "Numbers, pieces, units", H5)
            sheet_inv.write(row, 15, round(rec.amount_untaxed,0), H5)
            sheet_inv.write(row, 16, rec.amount_tax, H5)
            # sheet_inv.write(row, 20, rec.amount_total, H5)
            sheet_inv.write(row, 22, "" if rec.amount_tax else "6th Schd Table I", H5)
            sheet_inv.write(row, 23, "" if rec.amount_tax else "120", H5)
            row += 1

        ##########Adjusting column width######################
        sheet_inv.set_column(6, 0, 5)
        sheet_inv.set_column(6, 1, 12)
        sheet_inv.set_column(6, 7, 20)

        # sheet.insert_image('A1', r'/opt/odoo13/custom_addons/ta_hrm/static/images/logo.png', {'x_scale': 0.5, 'y_scale': 0.5})
        sheet_inv.write(1, 5, "Tax Report", H1)
        sheet_inv.write(3, 3, "From:", H3)
        sheet_inv.write(3, 5, "To:", H3)
        sheet_inv.write(3, 4, data['date_from'], date_format2)
        sheet_inv.write(3, 6, data['date_to'], date_format2)
        # ________________________________________________________________________________
        # #############################  Credit Note ###############################################
        #################### Headings  Inv ##############################
        sheet_credit_note.write(6, 0, "Sr.", H4)
        sheet_credit_note.write(6, 1, "Buyer NTN", H4)
        sheet_credit_note.write(6, 2, "Buyer Name", H4)
        sheet_credit_note.write(6, 3, "Buyer Type", H4)
        sheet_credit_note.write(6, 4, "Sale Origination Province of Supplier", H4)
        sheet_credit_note.write(6, 5, "Destination Province", H4)
        sheet_credit_note.write(6, 6, "Document Type", H4)
        sheet_credit_note.write(6, 7, "Document Number", H4)
        sheet_credit_note.write(6, 8, "Document Date", H4)
        sheet_credit_note.write(6, 9, "HS Code", H4)
        sheet_credit_note.write(6, 10, "Sale Type", H4)
        sheet_credit_note.write(6, 11, "Rate", H4)  # Tax Rate
        sheet_credit_note.write(6, 13, "Quantity", H4)  # Total Invoice Quantity
        sheet_credit_note.write(6, 14, "UOM", H4)
        sheet_credit_note.write(6, 15, "Value of Sales Excluding Sales Tax", H4)
        sheet_credit_note.write(6, 16, "Sales Tax", H4)
        sheet_credit_note.write(6, 17, "Fixed Value or Retail Price", H4)
        sheet_credit_note.write(6, 18, "Extra Tax", H4)
        sheet_credit_note.write(6, 19, "Further Tax", H4)
        sheet_credit_note.write(6, 20, "Total Value of Sales", H4)
        sheet_credit_note.write(6, 21, "ST Withheld at Source", H4)
        sheet_credit_note.write(6, 22, "SRO No. / Schedule No. ", H4)
        sheet_credit_note.write(6, 23, "Item S.No.", H4)
        # ##################################/////////////////////#####################################
        row = 7
        sr_number = 0
        for rec in account_move_credit_note:
            sr_number += 1
            sheet_credit_note.write(row, 0, sr_number, H5)
            sheet_credit_note.write(row, 1,
                            rec.partner_id.ntn if rec.partner_id.ntn else rec.partner_id.cnic if rec.partner_id.cnic else "-",
                            H5)
            sheet_credit_note.write(row, 2, rec.partner_id.name, H5)
            sheet_credit_note.write(row, 4, "Punjab", H5)
            sheet_credit_note.write(row, 5, rec.partner_id.state_id.name if rec.partner_id.state_id else "-", H5)
            sheet_credit_note.write(row, 6, "Credit Note", H5)
            sheet_credit_note.write(row, 7, rec.name, H5)
            sheet_credit_note.write(row, 8, rec.invoice_date, date_format)
            # get max hs code amount line
            list_line_amount = []
            max_hscode = ""
            for line in rec.invoice_line_ids:
                list_line_amount.append(line.price_subtotal)
                if max(list_line_amount) == line.price_subtotal:
                    max_hscode = line.product_id.x_hscode_description
            sheet_credit_note.write(row, 9, max_hscode, H5)
            sheet_credit_note.write(row, 10, "Goods at standard rate (default)" if rec.amount_tax else "Exempt goods", H5)
            if rec.amount_tax:
                sheet_credit_note.write(row, 11, 0.17, H5_percentage)
            else:
                sheet_credit_note.write(row, 11, "Exempt", H5)
            sheet_credit_note.write(row, 13, sum(rec.invoice_line_ids.mapped('quantity')), H5_float)
            sheet_credit_note.write(row, 14, "Numbers, pieces, units", H5)
            sheet_credit_note.write(row, 15, round(rec.amount_untaxed,0), H5)
            sheet_credit_note.write(row, 16, rec.amount_tax, H5)
            # sheet_credit_note.write(row, 20, rec.amount_total, H5)
            sheet_credit_note.write(row, 22, "" if rec.amount_tax else "6th Schd Table I", H5)
            sheet_credit_note.write(row, 23, "" if rec.amount_tax else "120", H5)
            row += 1

        ##########Adjusting column width######################
        sheet_credit_note.set_column(6, 0, 5)
        sheet_credit_note.set_column(6, 1, 12)
        sheet_credit_note.set_column(6, 7, 20)

        # sheet.insert_image('A1', r'/opt/odoo13/custom_addons/ta_hrm/static/images/logo.png', {'x_scale': 0.5, 'y_scale': 0.5})
        sheet_credit_note.write(1, 5, "Tax Credit Note Report", H1)
        sheet_credit_note.write(3, 3, "From:", H3)
        sheet_credit_note.write(3, 5, "To:", H3)
        sheet_credit_note.write(3, 4, data['date_from'], date_format2)
        sheet_credit_note.write(3, 6, data['date_to'], date_format2)
        # ________________________________________________________________________________
