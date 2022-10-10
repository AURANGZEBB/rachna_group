# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "This module is for misc customization in V14",
    "author": "AB",
    "version": "14.0.0.0.1",
    "summary": "Misc. Customization"
    "requirements.",
    "website": "www.ta.net",
    "category": "other",
    "depends": ['base','sale_management','sale_order_type', 'account'
                ],
    "data": [
        # "security/ir.model.access.csv",
        # "views/brand.xml",
        "reports/reports_call.xml",
        "views/extend_res_partner.xml",
        "views/extend_res_users.xml",
        "views/menu_and_view_partner_khi.xml",
        "views/sale_order_inherit.xml",
        "views/stock_picking_extend.xml",
        "views/account_move_extend.xml",
        "views/account_payment_extend.xml",
        "views/sale_order_type_extend.xml",
    ],
    "demo": [],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
