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

from openerp import models, fields


class project_issue(models.Model):

    _inherit = 'project.issue'

    task_ids = fields.Many2many('project.task', string='Tasks')
    feature_id = fields.Many2one('project.scrum.feature')


class project_task(models.Model):

    _inherit = 'project.task'
    tickets_ids = fields.Many2many('project.issue', string='Tickets')


class project_feature(models.Model):

    _inherit = 'project.scrum.feature'

    tickets_ids = fields.One2many(
        'project.issue', 'feature_id', string='Tickets')
