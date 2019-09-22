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

     @api.multi
     def generate_laporan_harian(self):
          #prepare template
          tpl = self.env['mail.template'].search(
            [('name', '=', 'Laporan Harian Bengkel')])
          data = tpl.render_template(
            tpl.body_html, 'simontir.lapharian', self.id, post_process=False)
          #data omset penjualan
          so = self.env['sale.order'].sudo().search([
               ('date_order', '=', self.tglLap)])
          self.printLap = data