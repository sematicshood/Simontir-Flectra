# -*- coding: utf-8 -*-

from flectra import models, fields, api

class roles_users(models.Model):
    _inherit = 'sale.order'

    x_estimasi_waktu    =   fields.Char()
    x_nomer_polisi      =   fields.Char()
    x_tipe_kendaraan    =   fields.Char()
    x_antrian_service   =   fields.Char()
    x_waktu_mulai       =   fields.Datetime()