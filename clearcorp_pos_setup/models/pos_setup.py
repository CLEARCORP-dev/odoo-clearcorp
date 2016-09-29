# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class base_configuration(models.TransientModel):
    _name = 'pos.config.settings'
    _inherit = 'res.config.settings'


# Modules Pos
    module_product_label = fields.Boolean(
        'product_label',
        help="""Installs the product_label.""")
