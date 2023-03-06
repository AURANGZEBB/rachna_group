{
    'name': 'Custom Party Ledger',
    'version': '1.0',
    'category': 'Invoicing',
    'summary': 'Custom Party Ledger Report',
    'description': 'This module provides a report to list all invoices or invoices of a specific customer.',
    'author': 'Your Name',
    'website': 'https://your-website.com',
    'depends': ['base', 'web', 'account'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/extend_sale_order_view.xml',
        # 'views/invoices_list_report.xml',
        'views/custom_action_js.xml',
        # 'wizard/ins_invoices_list.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'account_dynamic_reports/static/src/scss/dynamic_common_style.scss',
            'ta_report_dynamic/static/src/css/style.scss',
            # 'new_dynamic_report/static/src/js/report.js',
            # 'new_dynamic_report/static/src/js/components/partner_order_summary.js',
            'ta_report_dynamic/static/src/js/report_ledger.js',
            # 'account_dynamic_reports/static/src/js/script.js',
            # 'account_dynamic_reports/static/src/js/select2.full.min.js',
        ],
        'web.assets_qweb': [
            'ta_report_dynamic/static/src/xml/ledger.xml',
        ]
    },
    'license': 'OPL-1',
    'qweb': [
            'static/src/xml/ledger.xml',
             ],
    'installable': True,
    'auto_install': False,
}
