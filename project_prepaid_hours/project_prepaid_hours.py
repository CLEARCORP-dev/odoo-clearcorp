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
    
    date = fields.Datetime('Date:')
    quatity = fields.Float('Quantity', required=True)
    group_id = fields.Many2one('account.analytic.prepaid_hours')
    
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
    
class account_analytic_quantity_prepaid_hours_approval_line (models.Model):
    _name = 'account.analytic.prepaid_hours_approval_line'
    
    prepaid_hours_id = fields.Many2one('account.analytic.prepaid_hours')
    approval_id = fields.One2many('account.analytic.prepaid_hours_approval','approval_line_id')
    work_type_id = fields.Many2one('project.work.type')
    requested_hours = fields.Float('Feature hours')
    extra_hours = fields.Float('Extra hours')
    extra_amount = fields.Float('Extra amount')
     
     
class account_analytic_prepaid_hours_approval(models.Model):
    _name = 'account.analytic.prepaid_hours_approval'
    
    ticket_id = fields.Many2one('project.issue', string='Ticket')
    sequence = fields.Char('sequence')
    user_id = fields.Many2one('res.partner', string='User')
    date = fields.Date('Date')
    state = fields.Selection([('2b_approved', 'To approved'), ('approved', 'Approved'), ('rejected', 'Rejected')], string='State', default='2b_approved')
    approval_line_id = fields.Many2one('account.analytic.prepaid_hours_approval_line')

class account_analitic_account(models.Model):

    _inherit = 'account.analytic.account'
    
    acc_analytic_qty_grp_ids = fields.One2many('account.analytic.prepaid_hours', 'analitic_account_id')
    
     
class invoice_type (models.Model):
    _inherit = 'invoice.type'
    
    acc_analytic_qty_grp_id = fields.Many2one('account.analytic.prepaid_hours')


