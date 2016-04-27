# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from datetime import date
from lxml import etree


_TABLE = """
<group>
    <div style="padding-bottom:16px">
        <h2 style="display:inline; margin-right:24px">Approval</h2>
        <span>
            Estado
            <button style="margin-left:16px"
                name="" string="Approve" />
        </span>
    </div>
    <table>
        <thead>
            <tr>
                <th></th>
                <th style="text-align:right">%s</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Horas Bolsa</td>
                <td style="text-align:right">%s</td>
            </tr>
            <tr>
                <td>Horas Consumidas</td>
                <td style="text-align:right">-</td>
            </tr>
            <tr style="border-top:1px solid black">
                <td style="padding-bottom:16px">
                    <b>Horas Restantes</b>
                </td>
                <td style="text-align:right">
                    <b>-</b>
                </td>
            </tr>
            <tr>
                <td>
                    <b>Horas por aprobar</b>
                </td>
                <td style="text-align:right">
                    <b>SUMA DE OTROS APPROVALS</b>
                </td>
            </tr>
            <tr>
                <td>
                    <b>Horas requeridas</b>
                    <ul style="list-style-type:none">
                        <li>%s</li>
                    </ul>
                </td>
                <td style="text-align:right">
                    <b>SUMA</b>
                    <ul style="list-style-type:none">
                        <li>%s</li>
                    </ul>
                </td>
            </tr>
        </tbody>
    </table>
    </group>"""


class account_analytic_prepaid_hours (models.Model):
    """Hours groups"""
    _name = 'account.analytic.prepaid_hours'

    name = fields.Char('Name', required=True)
    quantity = fields.Float('Quantity', required=True)
    analitic_account_id = fields.Many2one(
        'account.analytic.account', string='Analytic Account')
    date = fields.Datetime('Date', required=True)
    active = fields.Boolean('Active', default=True)


class account_analytic_prepaid_hours_assigment (models.Model):
    _name = 'account.analytic.prepaid_hours.assigment'

    date = fields.Datetime('Date:', required=True)
    quantity = fields.Float('Quantity', required=True)
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


class PrepaidHoursApproval(models.Model):
    _name = 'account.analytic.prepaid_hours_approval'

    @api.model
    def _default_sequence(self):
        approval_sequence =\
            self.env['account.analytic.prepaid_hours_approval'].search_count(
                [('ticket_id', '=', self.id)])
        return approval_sequence + 1

    ticket_id = fields.Many2one('project.issue', string='Ticket')
    sequence = fields.Integer('sequence', default=_default_sequence)
    user_id = fields.Many2one('res.partner', string='User')
    date = fields.Date('Date')
    state = fields.Selection([('2b_approved', 'To approved'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected')],
                             string='State', default='2b_approved')
    approval_line_ids = fields.One2many(
        'account.analytic.prepaid_hours_approval_line', 'approval_id',
        string='Approval lines')
    approval_values = fields.One2many(
        'account.analytic.prepaid_hours_approved_values', 'approval_id',
        string='Approval values')

    def _get_table(self):
        _TABLE = """
<group>
    <div style="padding-bottom:16px">
        <h2 style="display:inline; margin-right:24px">Approval</h2>
        <span>
            Estado
            <button style="margin-left:16px"
                name="" string="Approve" />
        </span>
    </div>
    <table>
        <thead>
            <tr>
                <th></th>
                <th style="text-align:right">%s</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Horas Bolsa</td>
                <td style="text-align:right">%s</td>
            </tr>
            <tr>
                <td>Horas Consumidas</td>
                <td style="text-align:right">-</td>
            </tr>
            <tr style="border-top:1px solid black">
                <td style="padding-bottom:16px">
                    <b>Horas Restantes</b>
                </td>
                <td style="text-align:right">
                    <b>-</b>
                </td>
            </tr>
            <tr>
                <td>
                    <b>Horas por aprobar</b>
                </td>
                <td style="text-align:right">
                    <b>SUMA DE OTROS APPROVALS</b>
                </td>
            </tr>
            <tr>
                <td>
                    <b>Horas requeridas</b>
                    <ul style="list-style-type:none">
                        <li>%s</li>
                    </ul>
                </td>
                <td style="text-align:right">
                    <b>SUMA</b>
                    <ul style="list-style-type:none">
                        <li>%s</li>
                    </ul>
                </td>
            </tr>
        </tbody>
    </table>
    </group>"""

    def _get_approval_lines(self):
        lines = {
            'hours': '',
            'names': ''
        }
        for line in self.approval_line_ids:
            lines['names'] += '<li>%s</li>', line.work_type_id
            lines['hours'] += '<li>%s</li>', line.requested_hours
        return lines

    def _prepaid_hours(self):
        prepaid_hours = {
            'quantity': '',
            'names': ''
        }
        for prepaid in self.ticket_id.project_id.analytic_account_id.prepaid_hours_id:
            prepaid_hours['quantity'] +=\
                '<td style="text-align:right">%s</td>', prepaid.quantity
            prepaid_hours['names'] +=\
                '<td style="text-align:right">%s</td>', prepaid.name

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):

        if self._context is None:
            self._context = {}
        res = super(PrepaidHoursApproval, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=False)
        print "\n fields view get prepaid_hours_approval res: ",  res, "\n"
        doc = etree.fromstring(res['arch'])
        table = etree.fromstring(_TABLE)
        print etree.tostring(table, pretty_print=True)
        for node in doc.iter():
            if node.tag == 'sheet':
                node.append(table)
                break
            print node.tag, type(node)
        print etree.tostring(doc, pretty_print=True)
        res['arch'] = etree.tostring(doc, pretty_print=True)
        return res


class account_analitic_account(models.Model):

    _inherit = 'account.analytic.account'

    prepaid_hours_id = fields.One2many(
        'account.analytic.prepaid_hours', 'analitic_account_id')

    def create_account_analytic_prepaid_hours_assigment(self):
        today = date.today().strftime('%Y-%m-%d')
        contracts = self.env['account.analytic.account'].search([])
        prepaid_hours_id =\
            self.env['account.analytic.prepaid_hours'].search([])
        prepaid_hours_assigment =\
            self.env['account.analytic.prepaid_hours.assigment']
        for contract in contracts:
            for qty_qroup in prepaid_hours_id:
                if qty_qroup.analitic_account_id.id == contract.id:
                    vals = {
                        'date': today,
                        'quantity': qty_qroup.quantity,
                        'group_id': qty_qroup.id,
                    }
                    prepaid_hours_assigment.create(vals)
        return True

    @api.model
    def create_account_analytic_prepaid_hours_assigment_api7(self):
        self.create_account_analytic_prepaid_hours_assigment()


class invoice_type (models.Model):
    _inherit = 'invoice.type'

    prepaid_hours_id = fields.Many2one(
        'account.analytic.prepaid_hours', string="Prepaid hours")
