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

from openerp import models, fields, api
from datetime import date

class account_analytic_prepaid_hours (models.Model):
    _name = 'account.analytic.prepaid_hours'

    name = fields.Char('Name', required=True)
    quatity = fields.Float('Quantity', required=True)
    analitic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    active = fields.Boolean('Active', default=True)

class account_analytic_prepaid_hours_assigment (models.Model):
    _name = 'account.analytic.prepaid_hours.assigment'

    date = fields.Datetime('Date:', required=True)
    quatity = fields.Float('Quantity', required=True)
    group_id = fields.Many2one('account.analytic.prepaid_hours', required=True)

class account_analytic_quantity_prepaid_hours_approved_values (models.Model):
    _name = 'account.analytic.prepaid_hours_approved_values'

    prepaid_hours_id = fields.Many2one('account.analytic.prepaid_hours')
    prepaid_hours = fields.Float('Prepaid hours')
    expent_hours = fields.Float('Expent hours')
    remaining_hours = fields.Float('Remaining hours')
    tobe_approve = fields.Float('To be approve hours')
    requested_hours = fields.Float('Feature hours')
    extra_hours = fields.Float('Extra hours')
    extra_amount = fields.Float('Extra amount')
    approval_id = fields.Many2one('account.analytic.prepaid_hours_approval')

class account_analytic_quantity_prepaid_hours_approval_line (models.Model):
    _name = 'account.analytic.prepaid_hours_approval_line'

    prepaid_hours_id = fields.Many2one('account.analytic.prepaid_hours')
    approval_id = fields.Many2one('account.analytic.prepaid_hours_approval')
    work_type_id = fields.Many2one('project.work.type')
    requested_hours = fields.Float('Feature hours')
    extra_hours = fields.Float('Extra hours')
    extra_amount = fields.Float('Extra amount')


class account_analytic_prepaid_hours_approval(models.Model):
    _name = 'account.analytic.prepaid_hours_approval'

    ticket_id = fields.Many2one('project.issue', string='Ticket')
    sequence = fields.Integer('sequence')
    user_id = fields.Many2one('res.partner', string='User')
    date = fields.Date('Date')
    state = fields.Selection([('2b_approved', 'To approved'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected')],
                              string='State', default='2b_approved')
    approval_line_ids = fields.One2many('account.analytic.prepaid_hours_approval','approval_line_ids')
    approval_values = fields.One2many('account.analytic.prepaid_hours_approved_values','approval_id')

    def _get_sequence(self):
        approval_sequence = self.env['account.analytic.prepaid_hours_approval'].search_count([('ticket_id','=',self.id)])
        return approval_sequence + 1

    _defaults = {
                'sequence': _get_sequence,
                }

class account_analitic_account(models.Model):

    _inherit = 'account.analytic.account'

    acc_analytic_qty_grp_ids = fields.One2many('account.analytic.prepaid_hours'
                                               , 'analitic_account_id')

    def create_account_analytic_prepaid_hours_assigment(self):
        today = date.today().strftime('%Y-%m-%d')
        contracts = self.env['account.analytic.account'].search([])
        acc_analytic_qty_grp_ids = self.env['account.analytic.prepaid_hours'].search([])
        prepaid_hours_assigment = self.env['account.analytic.prepaid_hours.assigment']
        for contract in contracts:
            for qty_qroup in acc_analytic_qty_grp_ids:
                if qty_qroup.analitic_account_id.id == contract.id:
                    vals = {
                          'date': today,
                          'quatity': qty_qroup.quatity,
                          'group_id': qty_qroup.id,
                           }
                    prepaid_hours_assigment.create(vals)
        return True

    @api.model
    def create_account_analytic_prepaid_hours_assigment_api7(self):
        self.create_account_analytic_prepaid_hours_assigment()

class invoice_type (models.Model):
    _inherit = 'invoice.type'

    acc_analytic_qty_grp_id = fields.Many2one('account.analytic.prepaid_hours')
