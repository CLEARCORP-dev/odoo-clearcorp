# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import date


class account_analitic_account(models.Model):

    _inherit = 'account.analytic.account'

    currency_invoice = fields.Many2one('res.currency')


class feature(models.Model):

    _inherit = 'project.scrum.feature'

    state = fields.Selection([('draft', 'New'), ('open', 'In Progress'),
                             ('cancelled', 'Cancelled'), ('done', 'Done'),
                             ('quote_pending', 'Quote Pending'),
                             ('quoted', 'Quoted')],
                             'Status', required=True)


class issue(models.Model):

    _inherit = 'project.issue'

    group_approved = fields.One2many(
        'account.analytic.prepaid_hours_approval', 'ticket_id',
        string="Group approved")

    def _get_prepaid_hours(self):
        self.feature_id.work_type

    def _values(self, prepaid_hours_id):
        used_time = 0
        tobeapprove_time = 0
        approval_lines_obj = self.env[
            'account.analytic.prepaid_hours_approval_line'].search(
                [('prepaid_hours_id', '=', prepaid_hours_id)])
        for approval_line in approval_lines_obj:
            if approval_line.approval_id.state == 'approved':
                    used_time = used_time + approval_line.requested_hours
            else:
                if approval_line.approval_id.state == '2b_approved':
                    tobeapprove_time = tobeapprove_time +\
                        approval_line.requested_hours
        remaining_time = prepaid_hours_id.quantity - used_time
        return {
            'used_time': used_time,
            'tobeapprove_time': tobeapprove_time,
            'remaining_time': remaining_time,
        }

    def _calculate_extra_amount(self):
        _type = self.feature_id
        _price = self.project_id.analytic_account_id.invoice_type_id.search(
            [('name', '=', '')]).product_price

    def _create_approval_values(self, approval_id, prepaid_hours_id):
        _approval_values_obj = self.env[
            'account.analytic.prepaid_hours_approved_values']
        values = self._values(prepaid_hours_id)
        _approval_values_values = {
            'prepaid_hours_id': prepaid_hours_id,
            'prepaid_hours': prepaid_hours_id.quantity,
            'expent_hours': values['used_time'],
            'remaining_hours': values['remaining_time'],
            'tobe_approve': values['tobeapprove_time'],
            'requested_hours': self.feature_id.expected_hours,
            'extra_hours': values['remaining_time'] -
            self.feature_id.expected_hours,
            # 'extra_amount':,
            'approval_id': approval_id,
        }

    def _create_approval_line(self, approval_id):
        _feature_obj = self.env['project.scrum.feature'].browse(
            self.feature_id.id)
        _approval_line_obj = self.env[
            'account.analytic.prepaid_hours_approval_line']
        for hour_type in self.feature_obj.hour_ids:
            _ana_acc = self.project_id.analytic_account_id
            prepaid_hours_id = _ana_acc.acc_analytic_qty_grp_ids.search(
                [('name', '=', hour_type.name)]
                )[0].acc_analytic_qty_grp_id.id
            _approval_line_values = {
                'prepaid_hours_id': prepaid_hours_id,
                'approval_id': approval_id,
                'work_type_id': hour_type.id,
                'requested_hours': self.feature_id.expected_hours,
                # 'extra_hours': self._create_approval_line(prepaid_hours_id)
            }

    def _create_approvals(self):
        today = date.today().strftime('%Y-%m-%d')
        _approval_obj = self.env['account.analytic.prepaid_hours_approval']
        _approval_values = {
            'ticket_id': self.id,
            'user_id': self.user_id.id,
            'date': today,
            'state': '2b_approved',
        }

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):

        if self._context is None:
            self._context = {}
        res = super(issue, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=False)
        record_id = self._context and self._context.get(
            'active_id', False) or False
        active_model = self._context.get('active_model')
        if not view_type == 'form' or not record_id or (
                active_model and active_model != 'project.issue'):
            return res
        return res
