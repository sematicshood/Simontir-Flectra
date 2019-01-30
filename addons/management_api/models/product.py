from flectra import models, fields

class product(models.Model):
    _inherit    =   'product.product'

    x_type_motor = fields.One2many('fleet.vehicle.model', 'id', string='Tipe Motor')