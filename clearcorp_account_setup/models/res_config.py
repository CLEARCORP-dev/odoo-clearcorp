# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class base_configuration(models.TransientModel):
    _name = 'account.config.settings'
    _inherit = 'res.config.settings'

 # Modules Account
    module_account_invoice_ticket = fields.Boolean(
        'account_invoice_ticket',
        help="""Installs the account_invoice_ticket.""")
    module_account_payment_report = fields.Boolean(
        'account_payment_report',
        help="""Installs the account_payment_report module.""")
    module_base_company_prefix = fields.Boolean(
        'base_company_prefix',
        help="""Installs the base_company_prefix module.""")
    module_partner_defaulter = fields.Boolean(
        'partner_defaulter',
        help="""Installs the partner_defaulter module.""")
