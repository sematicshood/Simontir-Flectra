from flectra import models, fields, api

class newSaleOrder(models.Model):
    _inherit = 'sale.order'

    jenis_motor = fields.Many2one('fleet.vehicle.model', string='Tipe Motor')
    no_rangka = fields.char(default=False, string="No Rangka")
    no_mesin = fields.char(default=False, string="No Mesin")
    km_masuk =fields.char(default=False, string="Odometer")
    tahun_motor=fields.char(default=False, string="Tahun")

