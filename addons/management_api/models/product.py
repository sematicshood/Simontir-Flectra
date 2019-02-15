from flectra import models, fields

class product(models.Model):
    _inherit    =   'product.product'

    x_type_motor = fields.Many2many('fleet.vehicle.model', string='Tipe Motor')