from flectra import models, fields

class productTemplate(models.Model):
    _inherit    =   'product.template'

    vehicle_models_ids = fields.Many2many('fleet.vehicle.model', string='Vehicle Models')
    minimal_km         = fields.Integer('Minimal KM', default=0)
    registrasi         = fields.Boolean('Registrasi', default=False)
    on_sale            = fields.Integer('Terjual', default=0)

class Product(models.Model):
    _inherit = 'product.product'

    _order = 'sales_count desc'