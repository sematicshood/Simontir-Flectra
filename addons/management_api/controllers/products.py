from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback

class ProductsAPIBentar(http.Controller):
    @http.route('/simontir/products/search', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def productSearch(self, barcode = None, name = None, description = None, type = None):
        res = []

        if barcode != None:
            res      = request.env['product.product'].sudo().search_read([('barcode', 'ilike', barcode), ('type', '=', type)], fields=['name', 'barcode', 'qty_available', 'list_price', 'type'])

        if name != None:
            res = request.env['product.product'].sudo().search_read([('name', 'ilike', name), ('type', '=', type)], fields=['name', 'barcode', 'qty_available', 'list_price', 'type'])

        if description != None:
            res = request.env['product.product'].sudo().search_read([('description', 'ilike', description), ('type', '=', type)], fields=['name', 'barcode', 'qty_available', 'list_price', 'type'])

        return valid_response(status=200, data={
                'count': len(res),
                'results': res
            })

    @http.route('/simontir/nopol/search', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def nopolSearch(self, nopol = None):
        res = []

        res      = request.env['fleet.vehicle'].sudo().search_read([('license_plate', 'ilike', nopol)], fields=['license_plate'])

        return valid_response(status=200, data={
                'count': len(res),
                'results': res
            })

    @http.route('/simontir/products/tes', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def nopolSearch(self, nopol = None):
        try:
            res = []

            tes = request.env['product.product'].sudo().search([('id','=',1)]).write({
                'x_type_motor': [(4,45)]
            })

            print(tes)

            res = request.env['product.product'].sudo().search_read([('id','=',1)])

            return valid_response(status=200, data={
                    'count': len(res),
                    'results': res
                })
        except Exception as identifier:
            print(traceback.format_exc())