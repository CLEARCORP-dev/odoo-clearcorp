# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-Today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp import models, fields, api


class MailMessage(models.Model):

    _inherit = 'mail.message'

    privacity = fields.Selection(
        [('private', 'Private'), ('public', 'Public')],
        'Privacity', default='public')

    @api.model
    def _notify(self, newid, force_send=False, user_signature=True):

        message = self.sudo().browse(newid)

        if message.privacity != 'private':
            return super(MailMessage, self)._notify(
                newid, force_send=force_send, user_signature=user_signature)

        notification_obj = self.env['mail.notification']
        partner_obj = self.env['res.partner']
        user_obj = self.pool.get('res.users')
        partners_to_notify = set([])

        # all followers of the mail.message document have to be added
        # as partners and notified if a subtype is defined
        # (otherwise: log message)
        if message.subtype_id and message.model and message.res_id:
            fol_obj = self.env['mail.followers']
            # browse as SUPERUSER because rules could
            # restrict the search results
            fol_ids = fol_obj.sudo().search([
                ('res_model', '=', message.model),
                ('res_id', '=', message.res_id)])
            partners_to_notify |= set(
                fo.partner_id.id for fo in fol_ids
                if message.subtype_id.id in [st.id for st in fo.subtype_ids]
            )

        # remove me from notified partners, unless the message
        # is written on my own wall
        if message.subtype_id and message.author_id and \
                message.model == 'res.partner' and \
                message.res_id == message.author_id.id:
            partners_to_notify |= set([message.author_id.id])
        elif message.author_id:
            partners_to_notify -= set([message.author_id.id])

        # all partner_ids of the mail.message have to be notified
        # regardless of the above (even the author if explicitly added!)
        if message.partner_ids:
            partners_to_notify |= set([p.id for p in message.partner_ids])

        clean_partners = []
        # clean partners to notify only internal users
        for partner in partner_obj.browse(list(partners_to_notify)):
            for user in partner.user_ids:
                if user_obj.has_group(self._cr, user.id, 'base.group_user'):
                    clean_partners.append(partner.id)

        # notify
        notification_obj._notify(
            newid, partners_to_notify=clean_partners,
            force_send=force_send, user_signature=user_signature
        )
        message.refresh()

        # An error appear when a user receive a notification without notifying
        # the parent message -> add a read notification for the parent
        if message.parent_id:
            # all notified_partner_ids of the mail.message have
            # to be notified for the parented messages
            partners_to_parent_notify = set(
                message.notified_partner_ids).difference(
                    message.parent_id.notified_partner_ids)
            for partner in partners_to_parent_notify:
                for user in partner.user_ids:
                    if user.has_group('base.group_user'):
                        notification_obj.create({
                            'message_id': message.parent_id.id,
                            'partner_id': partner.id,
                            'is_read': True,
                        })
        return True
