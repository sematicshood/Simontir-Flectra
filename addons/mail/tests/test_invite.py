# -*- coding: utf-8 -*-
# Part of Odoo, Flectra. See LICENSE file for full copyright and licensing details.

from flectra.addons.mail.tests.common import TestMail
from flectra.tools import mute_logger


class TestInvite(TestMail):

    @mute_logger('flectra.addons.mail.models.mail_mail')
    def test_invite_email(self):
        mail_invite = self.env['mail.wizard.invite'].with_context({
            'default_res_model': 'mail.test',
            'default_res_id': self.test_pigs.id
        }).sudo(self.user_employee.id).create({
            'partner_ids': [(4, self.user_portal.partner_id.id), (4, self.partner_1.id)],
            'send_mail': True})
        mail_invite.add_followers()

        # Test: Pigs followers should contain Admin, Bert
        self.assertEqual(self.test_pigs.message_partner_ids,
                         self.user_portal.partner_id | self.partner_1,
                         'invite wizard: Pigs followers after invite is incorrect, should be Admin + added follower')
        self.assertEqual(self.test_pigs.message_follower_ids.mapped('channel_id'),
                         self.env['mail.channel'],
                         'invite wizard: Pigs followers after invite is incorrect, should not have channels')

        # Test: (pretend to) send email and check subject, body
        self.assertEqual(len(self._mails), 2, 'invite wizard: sent email number incorrect, should be only for Bert')
        self.assertEqual(self._mails[0].get('subject'), 'Invitation to follow %s: Pigs' % self.env['mail.test']._description,
                         'invite wizard: subject of invitation email is incorrect')
        self.assertEqual(self._mails[1].get('subject'), 'Invitation to follow %s: Pigs' % self.env['mail.test']._description,
                         'invite wizard: subject of invitation email is incorrect')
        self.assertIn('%s invited you to follow %s document: Pigs' % (self.user_employee.name, self.env['mail.test']._description),
                      self._mails[0].get('body'),
                      'invite wizard: body of invitation email is incorrect')
        self.assertIn('%s invited you to follow %s document: Pigs' % (self.user_employee.name, self.env['mail.test']._description),
                      self._mails[1].get('body'),
                      'invite wizard: body of invitation email is incorrect')
