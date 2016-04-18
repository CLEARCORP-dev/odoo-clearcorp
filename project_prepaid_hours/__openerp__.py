# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": 'Project prepaid hours',
    "version": '8.0.1.0',
    "author": 'ClearCorp',
    "description": """""",
    'category': 'Project Management',
    'sequence': 10,
    'website': 'http://clearcorp.cr',
    'depends': ['base', 'project_work_type', 'account_analytic_analysis'],
    'data': ['views/project_prepaid_hours_view.xml',
              'data/project_prepaid_hours_data.xml'],
    'auto_install': False,
    'application': False,
    'installable': True,
    'license': 'AGPL-3',
}
