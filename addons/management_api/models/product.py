from flectra import models, fields

class productTemplate(models.Model):
    _inherit    =   'product.template'

    vehicle_models_ids = fields.Many2many('fleet.vehicle.model', string='Vehicle Models')