# -*- coding: utf-8 -*-

from flectra import models, fields, api


class invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    printer_data = fields.Text(string="Printer Data", required=False, )
    nopol = fields.Text(string="No Polisi", required=False, )
    mekanik = fields.Text(string="Mekanik", required=False, )
    type_motor = fields.Text(string="Type Motor", required=False, )
    saran_mekanik = fields.Text(string="Saran Mekanik", required=False, )
    km_berikutnya = fields.Text(string="KM Berikutnya", required=False, )

    @api.multi
    def generate_printer_data(self):
        tpl = self.env['mail.template'].search(
            [('name', '=', 'Dot Matrix Invoice')])
        data = tpl.render_template(
            tpl.body_html, 'account.invoice', self.id, post_process=False)
        so = self.env['sale.order'].sudo().search([
            ('name', '=', self.origin)])
        self.nopol = so.vehicle.license_plate
        self.mekanik = so.mekanik_id.name
        self.km_berikutnya = so.vehicle.odometer
        self.saran_mekanik = so.x_saran_mekanik
        self.type_motor = so.vehicle.model_id.name
        self.printer_data = data

    @api.multi
    def action_invoice_cancel(self):
        self.printer_data = ''
        return super(invoice, self).action_cancel()

    @api.multi
    def action_invoice_open(self):
        res = super(invoice, self).action_invoice_open()
        self.generate_printer_data()
        return res
