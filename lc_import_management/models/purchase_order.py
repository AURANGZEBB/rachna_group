from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    lc_number = fields.Many2one("lc.import", string="LC #")

    def action_create_invoice(self):
        rtn = super(PurchaseOrder, self).action_create_invoice()
        bill = self.env['account.move'].search([('id', '=', rtn['res_id'])])
        if bill and self.lc_number:
            bill.lc_number = self.lc_number
        return rtn

    def button_confirm(self):
        # Call the super method to confirm the order
        res = super().button_confirm()

        # Get the newly created stock picking
        picking = self.env['stock.picking'].search([('purchase_id', '=', self.id),('state', 'not in', ['cancel'])])
        for pick in picking:
            pick.write({'lc_number': self.lc_number})

        return res
