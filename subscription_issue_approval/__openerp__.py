# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": 'Subscription Issue Approval',
    "version": '9.0.1.0',
    "author": 'ClearCorp',
    "summary": """ Issue approved""",
    'category': 'Projects',
    'sequence': 10,
    'auto_install': False,
    'application': False,
    'installable': True,
    'license': 'AGPL-3',
    'website': 'http://clearcorp.cr',
    'depends': [
        'base', 'subscription_prepaid_hours', 'project_scrum_method',
        'project_scrum_feature_work_est'
    ],
    'data': [
        'views/subscription_issue_approval_view.xml'
    ]
}