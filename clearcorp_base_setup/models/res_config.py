# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class base_configuration(models.TransientModel):
    _name = 'base.config.settings'
    _inherit = 'res.config.settings'

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
    module_sale_exception_nostock = fields.Boolean(
        'sale_exception_nostock',
        help="""Installs the sale_exception_nostock module.""")
    module_email_template_qweb = fields.Boolean(
        'email_template_qweb',
        help="""Installs the email_template_qweb module.""")
    module_base_location = fields.Boolean(
        'base_location',
        help="""Installs the base_location module.""")
    module_base_location_geonames_import = fields.Boolean(
        'base_location_geonames_import',
        help="""Installs the base_location_geonames_import module.""")
    module_base_partner_merge = fields.Boolean(
        'base_partner_merge',
        help="""Installs the base_partner_merge module.""")
    module_partner_address_street3 = fields.Boolean(
        'partner_address_street3',
        help="""Installs the partner_address_street3 module.""")
    module_partner_contact_birthdate = fields.Boolean(
        'partner_contact_birthdate',
        help="""Installs the partner_contact_birthdate module.""")
    module_partner_contact_gender = fields.Boolean(
        'partner_contact_gender',
        help="""Installs the partner_contact_gender module.""")
    module_partner_contact_in_several_companies = fields.Boolean(
        'partner_contact_in_several_companies',
        help="""Installs the partner_contact_in_several_companies module.""")
    module_partner_contact_nationality = fields.Boolean(
        'partner_contact_nationality',
        help="""Installs the partner_contact_nationality module.""")
    module_partner_external_map = fields.Boolean(
        'partner_external_map',
        help="""Installs the partner_external_map module.""")
    module_partner_firstname = fields.Boolean(
        'partner_firstname',
        help="""Installs the partner_firstname module.""")
    module_partner_identification = fields.Boolean(
        'partner_identification',
        help="""Installs the partner_identification module.""")
