# -*- coding: utf-8 -*-

from flectra import models, fields, api

class roles_users(models.Model):
    _inherit = 'project.task'

    x_status    =   fields.Char()