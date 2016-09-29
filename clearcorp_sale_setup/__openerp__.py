# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'ClearCorp Sale Configuration',
    'summary': 'App to install modules Sale',
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
        'sale_order_discount',
        'sale_order_report',
    ],
    'data': [
        'views/sale_setup_view.xml',
    ],
}
