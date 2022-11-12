from odoo import models, fields, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    courier_number = fields.Char(string="Courier Number")
    other_detail = fields.Char(string="Detail")
    
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['courier_number'] = self.courier_number
        invoice_vals['other_detail'] = self.other_detail

        for line in invoice_vals['invoice_line_ids']:
            line.batch_number = line.sale_line_ids.batch_number.id

        return invoice_vals

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    batch_number = fields.Many2one("ta.batch", string="Batch Number")