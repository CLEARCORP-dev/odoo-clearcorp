# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class base_configuration(models.TransientModel):
    _name = 'hr.config.settings'
    _inherit = 'res.config.settings'


# Modules HR
    module_hr_contract_extended = fields.Boolean(
        'hr_contract_extended',
        help="""Installs the hr_contract_extended.""")
    module_hr_personnel_actions = fields.Boolean(
        'hr_personnel_actions',
        help="""Installs the hr_personnel_actions module.""")
    module_hr_wage_increase = fields.Boolean(
        'hr_wage_increase',
        help="""Installs the hr_wage_increase module.""")
