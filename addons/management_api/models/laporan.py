# -*- coding: utf-8 -*-

from flectra import models, fields, api
import hashlib
import datetime


class laporanBengkel(models.Model):
    # _name = 'management_api.laporanBengkel'
    _name = 'laporanBengkel'
    # _inherit = 'account.invoice'
    nama_laporan = fields.Text('Nama Laporan')
    #printer_data = fields.Text(string="Printer Data", required=False, )

    # @api.multi
    # def generate_printer_data(self):
    #     tpl = self.env['mail.template'].search(
    #         [('name', '=', 'Dot Matrix Invoice')])
    #     data = tpl.render_template(
    #         tpl.body_html, 'account.invoice', self.id, post_process=False)
    #
    #     self.printer_data = data
    #
    # @api.multi
    # def action_invoice_cancel(self):
    #     self.printer_data = ''
    #     return super(invoice, self).action_cancel()
    #
    # @api.multi
    # def action_invoice_open(self):
    #     res = super(invoice, self).action_invoice_open()
    #     self.generate_printer_data()
    #     return res
