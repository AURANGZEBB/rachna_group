from odoo import models, fields, api
import datetime
from datetime import date
from odoo.exceptions import ValidationError

class HrPayslip(models.Model):
    _inherit = "hr.payslip"


    def mass_compute_sheet(self):
        for rec in self:
            if rec.state == 'draft':
                rec.compute_sheet()
            else:
                raise ValidationError("You can compute only for draft payslips")