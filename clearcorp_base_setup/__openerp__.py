# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'ClearCorp Base Configuration',
    'summary': 'addons, modules',
    'version': '9.0.1.0',
    'category': 'ClearCorp Modules',
    'website': 'http://clearcorp.cr',
    'author': 'ClearCorp',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'base_setup',
        'base_export_manager',
        'base_optional_quick_create',
        'base_report_auto_create_qweb',
        'base_technical_features',
        'date_range',
        'scheduler_error_mailer',
        'web_access_rule_buttons',
        'web_dialog_size',
        'web_favicon',
        'web_sheet_full_width',
        'web_translate_dialog',
        'web_widget_many2many_tags_multi_selection',
        'mail_attach_existing_attachment',
        'mail_optional_autofollow',
        'l10n_cr_base',
        'l10n_cr_currency_rate_update',
        'l10n_cr_currency_rate_update_BCCR',
    ],
    'data': [
        'views/res_config_view.xml',
    ],
}
