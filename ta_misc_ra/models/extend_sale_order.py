from odoo import models, fields, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    courier_number = fields.Char(string="Courier Number")
    other_detail = fields.Char(string="Detail")
    batch_number = fields.Many2one("ta.batch", string="Batch Number")
    
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['batch_number'] = self.batch_number.id
        return invoice_vals