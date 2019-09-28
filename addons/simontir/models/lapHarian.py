from flectra import models, fields, api
import datetime
from datetime import datetime, timedelta


class LapHarian(models.Model):
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
    totalGo = fields.Integer()
    totalHr = fields.Integer()
    totalQs = fields.Integer()
    totalGop = fields.Integer()
    selisih = fields.Float()
    totalCash = fields.Float()
    totalEdc = fields.Float()
    catatan = fields.Text()
    company = fields.Many2one('res.company', string='Perusahaan')

    def getIdProduct(self, category):
        product = request.env['product.product'].sudo()

        return [p.id for p in product.search([
            ('categ_id', 'ilike', category)
        ])]

    @api.multi
    def generateLaporanHarian(self):
        da = datetime.strptime(self.tglLap, '%Y-%m-%d')
        d1 = datetime.strftime(da, "%Y-%m-%d 00:00:00")
        d2 = datetime.strftime(da, "%Y-%m-%d 23:59:59")

        so = self.env['sale.order'].sudo().search([('confirmation_date', '>=', d1),
                                                   ('confirmation_date', '<', d2), ('state', '=', 'done')])
        inv = self.env['account.invoice.line'].sudo().search([('create_date', '>=', d1),
                                                              ('create_date', '<', d2)])

        #product = self.env['product.product'].sudo()
        #product_service = [p.id for p in product.search([
        #    ('type', '=', 'service')]
        #)]

        x_omsetjasa = 0
        x_omsetglobal = 0
        x_omsetpart = 0
        x_omsetpartoli = 0
        x_omsetpartbusi = 0
        x_omsetkpboli = 0
        x_invblmlunas = 0
        ass_1 = 0
        ass_2 = 0
        ass_3 = 0
        ass_4 = 0
        for sol in so:
              if sol['x_kpb'] == '1':
                 ass_1 += 1
                 if sol['x_kpb'] == '2':
                    ass_2 += 1
                 if sol['x_kpb'] == '3':
                    ass_3 += 1
                 if sol['x_kpb'] == '4':
                    ass_4 += 1

        # x_omsetglobal += sol['amount_total']
            # print(x_omset)
            # print(sol['name'])
#TODO validasi status invoice lunas
#TODO validasi KPB khusus
        for invl in inv:
            # print(invl.name)
            nosonya = invl.origin
            sonya = self.env['sale.order'].sudo().search([
                ('name', '=', nosonya)])
            issokpb = sonya.x_kpb
            fakturnya = self.env['account.invoice'].sudo().search([
                ('id', '=', invl.invoice_id)])
            statusinv = fakturnya.state
            id_product = invl.product_id
            typeprod = id_product.type
            categprod = id_product.categ_id
            if statusinv == 'paid':  # validasi status invoice yg sudah dibayar
                if typeprod == 'service':  # validasi tipe produk yg jasa / service
                    x_omsetjasa += invl['price_total']
                else:  # validasi tipe produk yg stockable/sparepart
                    x_omsetpart += invl['price_total']
                    if categprod == 'Oli':  # validasi tipe part yg kategori oli
                        x_omsetpartoli += invl['price_total']
                        if issokpb > 0: # validasi tipe produk yg jasa / service utk oli khusus kpb
                           x_omsetkpboli += invl['price_total']
                    if categprod == 'Busi': # validasi tipe part yg kategori busi
                        x_omsetpartbusi += invl['price_total']
            else:
                x_invblmlunas += invl['price_total']

        self.omsetJasa = x_omsetjasa
        self.omsetPart = x_omsetpart
        self.omsetKpbOli = x_omsetkpboli
        self.biayaHarian = float(12000)
        self.omsetPartBusi = x_omsetpartbusi
        self.omsetPartOli = x_omsetpartoli
        self.omsetPos = float(1000000)
        self.omsetTotalJasa = float(self.omsetJasa) + float(self.omsetKpbOli)
        self.omsetTotalPart = self.omsetPartBusi + self.omsetPartOli + self.omsetPart
        self.totalAss1 = ass_1
        self.totalAss2 = ass_2
        self.totalAss3 = ass_3
        self.totalAss4 = ass_4
        # self.printLap = ' '
        tpl = self.env['mail.template'].search(
            [('name', '=', 'Laporan Harian Bengkel')])
        data = tpl.render_template(
            tpl.body_html, 'simontir.lapharian', self.id, post_process=False)
        self.printLap = data
