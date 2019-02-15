# -*- coding: utf-8 -*-

from flectra import models, fields, api

class roles_users(models.Model):
    _inherit = 'res.users'

    role            = fields.Selection([
        ('1', 'Manager'), ('2', 'Mekanik'), ('3', 'Asisten Mekanik'), ('4', 'Front Desk'), ('5', 'Tukang Cuci')
    ], string="Role", required=True)