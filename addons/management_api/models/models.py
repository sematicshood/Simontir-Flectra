# -*- coding: utf-8 -*-

from flectra import models, fields, api
import hashlib
import datetime

class management_api(models.Model):
    _name = 'management_api.management_api'

    name            = fields.Char(string="Name apps")
    client_api      = fields.Text(compute="_client_api", store=True)
    client_secret   = fields.Text(compute="_client_secret", store=True)

    @api.depends('name')
    def _client_api(self):
        now  = datetime.datetime.now().replace(microsecond=0).isoformat()
        text = self.name + ' - ' + now

        sha_signature = hashlib.sha256(text.encode()).hexdigest()

        self.client_api = sha_signature

    @api.depends('name')
    def _client_secret(self):
        now  = datetime.datetime.now().replace(microsecond=0).isoformat()
        text = now + ' - ' + self.name

        sha_signature = hashlib.sha256(text.encode()).hexdigest()

        self.client_secret = sha_signature