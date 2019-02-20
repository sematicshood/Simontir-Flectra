# -*- coding: utf-8 -*-

from flectra import models, fields, api

class roles_users(models.Model):
    _inherit = 'sale.order'

    x_estimasi_waktu    =   fields.Char()
    x_nopol             =   fields.Char()
    x_type_motor        =   fields.Char()
    x_tipe_kendaraan    =   fields.Char()
    x_antrian_service   =   fields.Char()
    x_warna             =   fields.Char()
    x_waktu_mulai       =   fields.Datetime()
    x_is_reject         =   fields.Boolean(default=False)
    x_is_wash           =   fields.Boolean(default=False)
    x_duration          =   fields.Char()
    mekanik_id          =   fields.Many2one('res.users', string='Mekanik')