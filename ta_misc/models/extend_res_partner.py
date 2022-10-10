from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    contact_person = fields.Char(string="Contact Person")
    ntn = fields.Char(string="NTN")
    cnic = fields.Char(string="CNIC")
    default_discount_percentage = fields.Float(string="Default Discount in %")
    is_khi = fields.Boolean(string="IS KHI")
    preferred_courier = fields.Many2one("courier.service.provider", string="Preferred Courier")
    booking_type = fields.Many2one("booking.type", string="Booking Type")
