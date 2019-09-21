from flectra import models, fields, api


class lapHarian(models.Model):
     _name = 'simontir.lapHarian'

     tglLap = fields.date()
     omsetJasa = fields.float()
     omsetKpbOli = fields.float()
     omsetTotalJasa = fields.float()
     omsetPart = fields.float()
     omsetPartOli = fields.float()
     omsetPartBusi = fields.float()
     omsetTotalPart = fields.float()
     omsetPos = fields.float()
     biayaHarian = fields.float()
     printLap = fields.Text()


     @api.multi
     def generate_report_data(self):
          #data omset penjualan
          so = self.env['sale.order'].sudo().search([
               ('tglLap', '=', self.origin)])