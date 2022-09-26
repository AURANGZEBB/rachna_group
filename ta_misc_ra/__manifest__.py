#############################################
###################################################################################

{
    'name': 'Misc Customizations',
    'summary': 'Odoo Community Backend Theme',
    'version': '15.0.1.0.1',
    'category': 'Other',
    'license': 'LGPL-3',
    'author': 'The Adepts',
    'website': 'http://www.ta.net',
    'contributors': [
        'Mathias Markl <mathias.markl@mukit.at>',
    ],
    'depends': ['base','mrp','sale_management'],
    'excludes': [
        'web_enterprise',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/ta_batch.xml',
        'views/extend_mrp_production.xml',
        'views/extend_sale_order.xml',
    ],
    'assets': {
        'web.assets_qweb': [],
        'web._assets_primary_variables': [],
        'web._assets_backend_helpers': [],
        'web.assets_backend': [],
    },
    'images': [],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'uninstall_hook': '_uninstall_reset_changes',
}
