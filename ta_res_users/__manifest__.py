#############################################
###################################################################################

{
    'name': 'TA Users Customization',
    'summary': 'Odoo Community Backend Theme',
    'version': '15.0.1.0.1',
    'category': 'Other',
    'license': 'LGPL-3',
    'author': 'The Adepts',
    'website': 'http://www.ta.net',
    'contributors': [
        'Mathias Markl <mathias.markl@mukit.at>',
    ],
    'depends': ['base'],
    'excludes': [
        'web_enterprise',
    ],
    'data': [
        'views/res_users.xml',
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
