from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *

class BoardsAPIBentar(http.Controller):
    @http.route('/simontir/getso', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    @authentication
    def getso(self):
        so = request.env['sale.order'].sudo().search([
            ('state','!=','done'),
            ('state','!=','cancel'),
        ], order="id asc")

        data = [{
            "no_polisi": s.x_nomer_polisi,
            "customer": s.partner_id[0].name,
            "tipe_kenadaraan": s.x_tipe_kendaraan,
            "status": s.state,
            "invoice": s.invoice_status,
            "antrian_service": s.x_antrian_service,
            "order_line": [{
                "name": o.name,
                "type": o.product_id[0].product_tmpl_id[0].type
            } for o in s.order_line]
        } for s in so]
        
        return valid_response(status=200, data={
                'count': len(data),
                'results': data
            })

    @http.route('/simontir/getso_mekanik', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    @authentication
    def getso_mekanik(self):
        so = request.env['sale.order'].sudo().search([
            ('state','=','sale'),
            ('invoice_status','=','no')
        ], order="id asc")

        data = [{
            "no_polisi": s.x_nomer_polisi,
            "customer": s.partner_id[0].name,
            "tipe_kenadaraan": s.x_tipe_kendaraan,
            "status": s.state,
            "invoice": s.invoice_status,
            "antrian_service": s.x_antrian_service,
            "name": s.name,
            "order_line": [{
                "name": o.name,
                "type": o.product_id[0].product_tmpl_id[0].type
            } for o in s.order_line]
        } for s in so]
        
        return valid_response(status=200, data={
                'count': len(data),
                'results': data
            })