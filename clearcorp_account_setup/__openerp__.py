# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'ClearCorp Account Configuration',
    'summary': 'App to install Account packages ClearCorp',
    'version': '9.0.1.0',
    'category': 'ClearCorp Modules',
    'website': 'http://clearcorp.cr',
    'author': 'ClearCorp',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'clearcorp_base_setup',
        'account_account_prefix',
        'account_invoice_discount',
        'account_invoice_report',
        'account_journal_extended_code',
        'account_move_rate',
        'account_move_rate_calculated',
    ],
    'data': [
        'views/res_config_view.xml',
    ],
}
