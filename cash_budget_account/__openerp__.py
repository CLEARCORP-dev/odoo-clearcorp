# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Cash Budget Account',
    'version': '8.0.1.2',
    'summary': "Goverment Institutions Cash Budget Account",
    'author': 'ClearCorp',
    'website': 'http://clearcorp.cr',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'account_account_extended_ccorp',
        'account_distribution_line',
        'account'
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_invoice_view.xml',
        'views/account_move_line.xml',
        'views/account_view.xml',
        ]
}
