import odoo.exceptions
from odoo import fields, models,api
import datetime

class AccountMove(models.Model):
    _inherit = "account.move"

    x_user_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    is_khi = fields.Boolean(string="Is KHI", related="x_user_id.is_khi")
    allowed_types = fields.Many2many("sale.order.type", string="Allowed Types", related="x_user_id.order_types")
    x_journal_ids = fields.Many2many("account.journal", string="Journals", related="x_user_id.journal_ids")
    x_remarks = fields.Text(string="Remarks")
    confirm_uid = fields.Many2one("res.users", string="Confirm UID")
    @api.model
    def create(self, vals_list):
        rtn = super(AccountMove, self).create(vals_list)
        if rtn.journal_id not in rtn.x_journal_ids:
            raise odoo.exceptions.ValidationError("The Selected Journal is Not Allowed")

        return rtn

    def action_post(self):
        rtn = super(AccountMove, self).action_post()
        users_with_no_initials = self.env['res.users'].search([('initials', '=', False)])
        if users_with_no_initials:
            raise odoo.exceptions.ValidationError("There are no '''Initials''' for some User(s) !!!!")
        else:
            self.confirm_uid = self.env.user.id
        return rtn

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    x_brand = fields.Many2one("ta.brand", related="product_id.x_brand", store=True)


class AccountPayment(models.Model):
    _inherit = "account.payment"

    x_partner_id = fields.Many2one("res.partner", string="Partner Custom")

    @api.onchange('x_partner_id')
    def onchange_x_partner_id(self):
        for rec in self:
            if rec.x_partner_id.parent_id:
                rec.partner_id = rec.x_partner_id.parent_id.id
            else:
                rec.partner_id = rec.x_partner_id.id