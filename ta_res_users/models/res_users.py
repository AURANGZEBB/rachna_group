from odoo import fields, models, api

class ResUsers(models.Model):
    _inherit = "res.users"

    show_my_dashboard = fields.Boolean(string="Show My Dashboard To Others")