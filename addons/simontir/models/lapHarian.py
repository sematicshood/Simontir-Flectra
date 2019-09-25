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
             else:
                 ass_4 += 1

        # x_omsetglobal += sol['amount_total']
            # print(x_omset)
            # print(sol['name'])

        for invl in inv:
            # print(invl.name)
            nosonya = invl.origin
            sonya = self.env['sale.order'].sudo().search([
                ('name', '=', nosonya)])

            id_product = invl.product_id
            typeprod = id_product.type
            if typeprod == 'service':
                x_omsetjasa += invl['price_total']
            else:
                x_omsetpart += invl['price_total']

        self.omsetJasa = x_omsetjasa
        self.omsetPart = x_omsetpart
        self.omsetKpbOli = float(100000)
        self.biayaHarian = float(12000)
        self.omsetPartBusi = float(120)
        self.omsetPartOli = float(29000)
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
