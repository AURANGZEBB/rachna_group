# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'LC Import Management',
    'version' : '1.2',
    'summary': 'LC Import',
    'sequence': 10,
    'description': """
Invoicing & Payments
====================
The specific and easy-to-use Invoicing system in Odoo allows you to keep track of your accounting, even when you are not an accountant. It provides an easy way to follow up on your vendors and customers.

You could use this simplified accounting in case you work with an (external) account to keep your books, and you still want to keep track of payments. This module also offers you an easy method of registering payments, without having to encode complete abstracts of account.
    """,
    'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/app/invoicing',
    'images' : [],
    'depends' : ['base','purchase','base_accounting_kit'],
    'data': [
        'security/ir.model.access.csv',
        'data/rules.xml',
        'views/lc_import.xml',
        'views/picking_extend.xml',
        'views/account_move_extend.xml',
        'views/account_payment_extend.xml',
        'views/purchase_order_extend.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web._assets_primary_variables': [],
        'web.assets_backend': [],
        'web.assets_frontend': [],
        'web.assets_tests': [],
        'web.qunit_suite_tests': [],
        'web.assets_qweb': [],
    },
    'license': 'LGPL-3',
}
