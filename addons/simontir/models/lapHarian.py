from flectra import models, fields, api
import datetime

class lapHarian(models.Model):
     _name = 'simontir.lapharian'

     tglLap = fields.Date()
     omsetJasa = fields.Float()
     omsetKpbOli = fields.Float()
     omsetTotalJasa = fields.Float()
     omsetPart = fields.Float()
     omsetPartOli = fields.Float()
     omsetPartBusi = fields.Float()
     omsetTotalPart = fields.Float()
     omsetPos = fields.Float()
     biayaHarian = fields.Float()
     printLap = fields.Text()
     kasir = fields.Many2one('res.users', string='Kasir')
     totalAss1 = fields.Integer()
     totalAss2 = fields.Integer()
     totalAss3 = fields.Integer()
     totalAss4 = fields.Integer()
     selisih = fields.Float()
     totalCash = fields.Float()
     totalEdc = fields.Float()
     catatan = fields.Text()
     company = fields.Many2one('res.company', string='Perusahaan')

     @api.multi
     def generate_laporan_harian(self):
          #prepare template
          tpl = self.env['mail.template'].search(
            [('name', '=', 'Laporan Harian Bengkel')])
          data = tpl.render_template(
            tpl.body_html, 'simontir.lapharian', self.id, post_process=False)
          #data omset penjualan = amount_total,state=done,confirmation_date
          #parameter x_kpb,
          saleorder            = self.env['sale.order'].sudo().search([
                               ('confirmation_date', '=', self.tglLap)])
          #saleorderline        = self.env['sale.order.line'].sudo().search([
          #                     ('date_order', '=', self.tglLap)])
          #Transaksi keuangan
          #account_line         =   self.env['account.invoice.line'].sudo()
          #account              =   self.env['account.invoice'].sudo()
          
          tot_omset = 0
          for so in saleorder:
               tot_omset = so['amount_total'] + tot_omset

          self.omsetJasa = tot_omset
          self.printLap = data