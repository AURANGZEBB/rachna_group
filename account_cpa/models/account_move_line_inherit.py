# -*- coding: utf-8 -*-
import datetime

from lxml import etree
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class AccountMoveLine(models.Model):
    inherit = "account.move.line"

    product_category = fields.Many2one("product.category", string="Product Category", related="product_id.categ_id")