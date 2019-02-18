# -*- coding: utf-8 -*-

from flectra import models, fields, api
import hashlib
import datetime

class management_api(models.Model):
    _name = 'vehicle.colors'

    color            = fields.Char()