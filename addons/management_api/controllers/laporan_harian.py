from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from datetime import datetime, timedelta

class LaporanHarian(http.Controller):
    def getIdProduct(self, category, company_id):
        product         =   request.env['product.product'].sudo()

        return [p.id for p in product.search([
            ('categ_id', 'ilike', category),
            ('company_id', '=', int(company_id))
        ])]

    @http.route('/simontir/laporan_harian', methods=['GET', 'OPTIONS'], cors="*", auth="none", type="http", csrf=False)
    def getLaporanHarian(self, date = None):
        try:
            fields_c        =   ['id']
            product         =   request.env['product.product'].sudo()
            template        =   request.env['product.template'].sudo()
            category        =   request.env['product.category'].sudo()

            product_service =   [p.id for p in product.search([
                ('type', '=', 'service')],
                ('company_id', '=', int(company_id))
            )]

            oli_kpb         =   self.getIdProduct("oli kpb", company_id)
            hgp             =   self.getIdProduct("hgp", company_id)
            oli             =   self.getIdProduct("oli", company_id)
            busi            =   self.getIdProduct("busi", company_id)

            account         =   request.env['account.invoice.line'].sudo()

            da    = datetime.strptime(date, '%Y-%m-%d')
            d     = da + timedelta(days=1)
        
            domain          =   [('create_date', '>=', date), ('create_date', '<', d.strftime('%Y-%m-%d')), ('company_id', '=', int(company_id))]
            fields          =   ['price_total', 'product_id']

            satu    = 0 
            dua     = 0
            empat   = 0
            lima    = 0
            enam    = 0
            
            st   = account.search_read(domain, fields=fields)

            for s in st:
                if s['product_id'] in product_service:
                    satu += s['price_total']

                    if s['product_id'] in oli_kpb:
                        dua += s['price_total']

                    if s['product_id'] in hgp:
                        empat += s['price_total']

                    if s['product_id'] in oli:
                        lima += s['price_total']

                    if s['product_id'] in busi:
                        enam += s['price_total']

            data = {
                "satu": satu,
                "dua": dua,
                "tiga": satu + dua,
                "empat": empat,
                "lima": lima,
                "enam": enam,
                "tujuh": empat + lima + enam
            }

            return valid_response(status=200, data={
                    'results': data
                })

        except Exception as identifier:
            print(traceback.format_exc())