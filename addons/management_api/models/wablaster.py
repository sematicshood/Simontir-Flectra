from flectra import models, fields, api
from flectra.exceptions import ValidationError
import re
import requests

class Wablaster(models.Model):
    _name = 'wablaster'

    phones      = fields.Many2many('res.partner', String='Nomer Telephone', ondelete='cascade')
    user_id     = fields.Many2one('res.users', default=lambda self: self.env.user)
    messages    = fields.Text('Messages')

    def sender(self, record):
        # print('='*100)
        account = self.env['wablaster.account'].search([])[0]
        for user in record[0].phones:
            url = "http://api.notifikasi.online/public/new_message/?key={}&username={}".format(account.api_key, account.username)
            if user.phone:
                data = {
                    'key': account.api_key, 
                    'target': user.phone, 
                    'message': record.messages
                }

                req = requests.post(url, data)
                print(user.phone)
                print(req)



class WablasterAccount(models.Model):
    _name = 'wablaster.account'

    username = fields.Char()
    email = fields.Char()
    phone_number = fields.Char()
    api_key = fields.Char()

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')