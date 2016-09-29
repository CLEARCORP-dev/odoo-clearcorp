# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class base_configuration(models.TransientModel):
    _name = 'sale.config.settings'
    _inherit = 'res.config.settings'


# Modules Sale
    module_sales_team_multicompany = fields.Boolean(
        'sales_team_multicompany',
        help="""Installs the sales_team_multicompany module.""")
    module_product_label = fields.Boolean(
        'product_label',
        help="""Installs the product_label module.""")
