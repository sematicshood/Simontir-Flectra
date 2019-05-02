# -*- coding: utf-8 -*-

from flectra import models, fields, api

class vehicleColor(models.Model):
    _name = 'vehicle.colors'

    color            = fields.Char(string='Vehicle_color', placeholder='Vehicle color', store=True, required=True, help="Vehicle color must be write with UPPERCASE")

    @api.onchange('color')
    def _color(self):
        try:
            print(self.color)
            self.color = str(self.color).upper() if self.color else ''
        except Exception as identifier:
            print(identifier)