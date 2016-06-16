# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Cash Budget',
    'version': '8.0.1.2',
    'summary': "Goverment Institutions Cash Budget",
    'author': 'ClearCorp',
    'website': 'http://clearcorp.cr',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'base', 'cash_budget_account'
        ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/budget_sequence.xml',
        'views/budget_view.xml',
        'views/budget_workflow.xml',
        'wizard/budget_import_catalog_view.xml',
        'wizard/budget_program_populate_view.xml'
        ]
}
