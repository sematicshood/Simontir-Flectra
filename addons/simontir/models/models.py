# -*- coding: utf-8 -*-

from flectra import models, fields, api


class simontir(models.Model):
     _name = 'simontir.simontir'

     nama           = fields.Char()
     test1          = fields.Integer()
     test2          = fields.Float(compute="_value_pc", store=True)
     description    = fields.Text()

     @api.depends('test2')
     def _value_pc(self):
         self.test2 = float(self.test1) / 100