# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class TicketInvoiceType (models.Model):
    _name = 'ticket.invoice.type'

    name = fields.Char('Name', required='True')
    ticket_type = fields.Selection(
        [('change_request', 'Change Request'),
         ('service_request', 'Service Request'),
         ('issue', 'Issue'), ('problem', 'Problem')],
        string='Issue Type', default='issue', required=True)
    # Determines if the issue is covered by the warranty
    warranty = fields.Boolean('Covered by the warranty?')

    # This relates the client's Subscription (contract) with the different
    # ticket invoice types.
    # todo check this isn't presented in the view
    contract_type_ids = fields.Many2many('sale.subscription')


class ProjectIssue(models.Model):
    _inherit = 'project.issue'
    
    @api.one
    @api.depends("project_id")
    def _compute_invoice_ticket(self):
        # Sets invoiced status
        if self.project_id:
            for ticket_kind in self.project_id.\
                    analytic_account_id.\
                    subscription_ids.ticket_invoice_type_ids:
                if ticket_kind.name == self.issue_type.name:
                    if ticket_kind.warranty:
                        self.invoiced = 'warranty'
                        return False
                    else:
                        self.invoiced = 'invoice'
                        return True

    issue_type = fields.Many2one('ticket.invoice.type', string='Type')
    invoiced = fields.Selection(
        [('invoice', 'Invoice'),
         ('warranty', 'Warranty'),
         ('2beinvoice', 'To be Invoiced'),
         ('invoiced', 'Invoiced')],
        string="Invoice", help="Task Invoice Status",
        compute='_compute_invoice_ticket', store=True)


class SaleSubscription(models.Model):

    _inherit = 'sale.subscription'
    ticket_invoice_type_ids = fields.Many2many('ticket.invoice.type')
