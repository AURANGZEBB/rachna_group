from odoo import fields, models,api,_
from odoo.tools import get_lang
from odoo.exceptions import ValidationError

class TaxReportWizard(models.TransientModel):
    _name = "tax.report.wizard"

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")

    def generate_tax_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        return self.env.ref("report_multi.action_tax_report_custom").report_action(self, data=data)
