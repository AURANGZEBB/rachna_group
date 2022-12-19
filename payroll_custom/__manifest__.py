# Copyright 2021 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Payroll Custom",
    "summary": "Payroll Custom",
    "version": "15.0.1.0.0",
    "category": "other",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "The Adepts",
    "maintainers": ["ta"],
    "license": "AGPL-3",
    "depends": [
            "hr",
            "hr_attendance",
            "report_xlsx",
            "hr_payroll_community",
            "hr_zk_attendance",
                ],
    "data": [
        "security/ir.model.access.csv",
        "views/attendance_list_inherit.xml",
        "views/payslip_extend.xml",
        "report/payroll_report_xlsx_call.xml",
        "report/payroll_report_wizard.xml",

    ],
}
