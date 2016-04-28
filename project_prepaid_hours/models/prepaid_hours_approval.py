# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
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

    def _get_approval_lines(self):
        lines = {
            'hours': '',
            'names': ''
        }
        ticket_id = self.env['project.issue'].browse(
            self._context.get('issue_id'))
        approval = ticket_id.prepaid_hours_approval_id[0]
        for line in approval.approval_line_ids:
            lines['names'] += '<li>%s</li>' % line.work_type_id.name
            lines['hours'] += '<li>%s</li>' % line.requested_hours
        print "\nLines: ", lines, self.approval_line_ids
        return lines

    def _get_prepaid_hours(self):
        prepaid_hours = {
            'quantity': '',
            'names': ''
        }
        ticket_id = self.env['project.issue'].browse(
            self._context.get('issue_id'))
        for prepaid in\
                ticket_id.project_id.analytic_account_id.prepaid_hours_id:
            quantity = '<td style="text-align:right">%s</td>' %\
                prepaid.quantity
            prepaid_hours['quantity'] += quantity
            name = '<td style="text-align:right">%s</td>' % prepaid.name
            prepaid_hours['names'] += name
        print "\nprepaid: ", prepaid_hours,
        return prepaid_hours

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
                <th></th>""" +\
            self._get_prepaid_hours()['names'] +\
            """</tr>
        </thead>
        <tbody>
            <tr>
                <td>Horas Bolsa</td>""" +\
            self._get_prepaid_hours()['quantity'] +\
            """
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
                    <ul style="list-style-type:none">""" +\
            self._get_approval_lines()['names'] +\
            """
                    </ul>
                </td>
                <td style="text-align:right">
                    <b>SUMA</b>
                    <ul style="list-style-type:none">""" +\
            self._get_approval_lines()['hours'] +\
            """
                    </ul>
                </td>
            </tr>
        </tbody>
    </table>
    </group>"""
        return _TABLE

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):

        if self._context is None:
            self._context = {}
        res = super(PrepaidHoursApproval, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=False)
        doc = etree.fromstring(res['arch'])
        table = etree.fromstring(self._get_table())
        print etree.tostring(table, pretty_print=True)
        for node in doc.iter():
            if node.tag == 'sheet':
                node.append(table)
                break
            print node.tag, type(node)
        print etree.tostring(doc, pretty_print=True)
        res['arch'] = etree.tostring(doc, pretty_print=True)
        return res
