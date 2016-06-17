# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Cash Budget Sale Stock',
    'version': '8.0.1.2',
    'summary': "Goverment Institutions Budget Stock",
    'author': 'ClearCorp',
    'website': 'http://clearcorp.cr',
    'category': 'Accounting & Finance/Sale/Stock',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'sale_stock',
        'sale',
        'cash_budget'
        ],
    'data': [
        'views/sale_view.xml',
        ]
}
