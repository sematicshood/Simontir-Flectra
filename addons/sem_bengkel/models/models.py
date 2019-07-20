# -*- coding: utf-8 -*-

from flectra import models, fields, api

 class sem_bengkel(models.Model):
     _inherit = 'sale'
     _name = 'sem_bengkel.sem_bengkel'

     #custom_field =field.Char(string='Custom Field')
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100