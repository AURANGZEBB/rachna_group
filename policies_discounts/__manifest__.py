# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Policies and Discounts',
    'version' : '1.2',
    'summary': 'Policies',
    'sequence': 11,
    'description': """
policies & Discounts
====================
The specific and easy-to-use Invoicing system in Odoo allows you to keep track of your accounting, even when you are not an accountant. It provides an easy way to follow up on your vendors and customers.

You could use this simplified accounting in case you work with an (external) account to keep your books, and you still want to keep track of payments. This module also offers you an easy method of registering payments, without having to encode complete abstracts of account.
    """,
    'category': 'Other',
    'website': 'https://www.ta.com',
    'images' : [],
    'depends' : ['sale_management'],
    'data': [
        #'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/rules.xml',
        'views/sale_policy_type.xml',
        'views/sale_policy_benefits.xml',
        'views/sale_policy.xml',
        'views/extend_sale_order.xml',
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
