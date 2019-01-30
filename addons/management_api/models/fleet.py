from flectra import models, fields

class fleet(models.Model):
    _inherit    =   'fleet.vehicle.log.services'

    x_mekanik = fields.Many2one('res.partner', string='Mekanik')