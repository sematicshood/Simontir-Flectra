from flectra import models, fields

class fleet(models.Model):
    _inherit    =   'fleet.vehicle.log.services'

    x_front_desk = fields.Many2one('res.users', string='Front Desk')
    x_mekanik    = fields.Many2one('res.users', string='Mekanik')

class fleet(models.Model):
    _inherit    =   'fleet.vehicle.model'

    x_group_motor   =   fields.Char()
    x_product_ids = fields.Many2many('product.template', string='Product Motor')