from odoo import models, fields, api, _


class TaBatch(models.Model):
    _name = "ta.batch"

    name = fields.Char(string="BATCH", required=1)