from odoo import models, fields, api
import datetime
from datetime import date

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    rule_present_and_halfday = fields.Boolean(string="Trace Presence and Halfday")
