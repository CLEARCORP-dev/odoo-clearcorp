# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Cash Budget HR Expense',
    'version': '8.0.1.2',
    'summary': "Goverment Institutions Cash Budget",
    'author': 'ClearCorp',
    'website': 'http://clearcorp.cr',
    'category': 'Accounting & Finance/Human Resources',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'expense_line_partner',
        'hr_expense',
        'cash_budget'
        ],
    'data': [
        'views/hr_expense_view.xml',
        'views/hr_expense_workflow.xml',
        ]
}
