# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Report Purchase Prediction",
    'summary': 'report purchase prediction',
    'version': '8.0.1.0',
    "website": "http://www.clearcorp.cr",
    'author': 'ClearCorp',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    "category": "Generic Modules/Inventory Control",
    "depends": ["base", "stock", "purchase"],
    'data': [
        "views/purchase_prediction_view.xml",
        "views/prediction_sequence.xml",
        "views/report_purchase_prediction.xml"
    ]
}
