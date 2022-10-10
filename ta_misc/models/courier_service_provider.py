from odoo import fields, models

class CourierServiceProvider(models.Model):
    _name = "courier.service.provider"

    name = fields.Char(string="Courier Service Provider", required=True)
