# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addons modules by CLEARCORP S.A.
#    Copyright (C) 2009-TODAY CLEARCORP S.A. (<http://clearcorp.co.cr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
	'name': 'Rent',
	'version': '1.1',
	'url': 'http://launchpad.net/openerp-ccorp-addons',
	'author': 'ClearCorp S.A.',
	'website': 'http://clearcorp.co.cr',
	'category': 'Rent',
	'description': """ClearCorp 'rent' module for real estate business.
	""",
	'depends': [
		'account',
		'l10n_cr_base',
		],
	'init_xml': [],
	'demo_xml': [],
	'update_xml': [
					'wizard/rent_make_group.xml',
					'wizard/rent_check_invoicing.xml',
					'rent_sequence.xml',
					'rent_view.xml', 
					'rent_data.xml',
					'rent_workflow.xml', 
					'rent_contract_report.xml',
					'security/rent_security.xml',
					'security/ir.model.access.csv',
				],
	'license': 'AGPL-3',
	'installable': True,
	'active': False,
}
