from odoo import fields, models

class BookingType(models.Model):
    _name = "booking.type"

    name = fields.Char(string="Booking Type", required=True)
