# -*- coding: utf-8 -*-

from flectra import models, fields, api

# class sem_custom_field_sales_order(models.Model):
#     _name = 'sem_custom_field_sales_order.sem_custom_field_sales_order'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
class SaleOrderInherited(models.Model):
    _inherit = 'sale.order'

    custom_field = fields.Char(string='Custom Field')
    x_estimasi_waktu = fields.Char()
    x_nopol = fields.Char()
    x_type_motor = fields.Char()
    x_tipe_kendaraan = fields.Char()
    x_antrian_service = fields.Selection(
        [('Reguler', 'Reguler'), ('Booking Service', 'Booking Service'), ('Express', 'Express')], string="Antrian Service")
    x_warna = fields.Many2one('vehicle.colors', string='Warna')
    x_waktu_mulai = fields.Datetime()
    x_is_reject = fields.Boolean(default=False)
    x_is_wash = fields.Boolean(default=False)
    x_duration = fields.Char()
    mekanik_id = fields.Many2one('res.users', string='Mekanik')
    checker_id = fields.Many2one('res.users', string='Final Check')
    x_kpb = fields.Selection([(1, 1), (2, 2), (3, 3), (4, 4)], string="Type KPB")
    x_service = fields.Selection(
        [('Ringan', 'Ringan'), ('Lengkap', 'Lengkap'), ('Turun Mesin', 'Turun Mesin')], string="Service Type")
    x_ganti_oli = fields.Boolean(default=False, string="Ganti Oli")
    x_ganti_part = fields.Boolean(default=False, string="Ganti part")
    x_claim = fields.Boolean(default=False, string="Claim")
    x_job_return = fields.Boolean(default=False, string="Job Return")
    x_service_kunjungan = fields.Boolean(default=False, string="Service Kunjungan")
    x_other_job = fields.Boolean(default=False, string="Other Job")
    x_spesial_program = fields.Boolean(default=False, string="Spesial Program")
