# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class adhoc_base_configuration(models.TransientModel):
    _name = 'base.config.settings'
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

    # Modules Sales
    module_sale_order_discount = fields.Boolean(
        'Customization from sale order to apply global discounts.',
        help="""Installs the sale_order_discount module.""")
    module_sale_order_report = fields.Boolean(
        'Sale order report in Qweb',
        help="""Installs the sale_order_report module.""")
    module_sales_team_multicompany = fields.Boolean(
        'sales_team_multicompany',
        help="""Installs the sales_team_multicompany module.""")
    module_product_label = fields.Boolean(
        'product_label',
        help="""Installs the product_label module.""")

    # Modules Base
    module_force_no_demo_data = fields.Boolean(
        'force_no_demo_data',
        help="""Installs the force_no_demo_data module.""")
    module_auth_signup_verify_email = fields.Boolean(
        'auth_signup_verify_email',
        help="""Installs the auth_signup_verify_email module.""")
    module_auth_supplier = fields.Boolean(
        'auth_supplier',
        help="""Installs the auth_supplier module.""")
    module_base_user_gravatar = fields.Boolean(
        'base_user_gravatar',
        help="""Installs the base_user_gravatar module.""")
    module_database_cleanup = fields.Boolean(
        'database_cleanup',
        help="""Installs the database_cleanup module.""")
    module_disable_odoo_online = fields.Boolean(
        'disable_odoo_online',
        help="""Installs the disable_odoo_online module.""")
    module_users_ldap_mail = fields.Boolean(
        'users_ldap_mail',
        help="""Installs the users_ldap_mail module.""")
    module_users_ldap_populate = fields.Boolean(
        'users_ldap_populate',
        help="""Installs the users_ldap_populate module.""")
    module_web_searchbar_full_width = fields.Boolean(
        'web_searchbar_full_width',
        help="""Installs the web_searchbar_full_width module.""")
    module_web_send_message_popup = fields.Boolean(
        'web_send_message_popup',
        help="""Installs the web_send_message_popup module.""")
    module_web_widget_timepicker = fields.Boolean(
        'web_widget_timepicker',
        help="""Installs the web_widget_timepicker module.""")
    module_sale_automatic_workflow = fields.Boolean(
        'sale_automatic_workflow',
        help="""Installs the sale_automatic_workflow module.""")
    module_sale_exception = fields.Boolean(
        'sale_exception',
        help="""Installs the sale_exception module.""")

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
