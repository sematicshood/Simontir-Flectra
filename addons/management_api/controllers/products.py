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
    def productSearch(self, barcode = None, name = None, description = None, type = None, vehicle = None):
        res    = []

        search = []

        fields = ['name', 'barcode', 'qty_available', 'list_price', 'type']

        if type != None:
            search.append(('type', '=', type))

        if barcode != None:
            search.append(('barcode', 'ilike', barcode))

        if name != None:
            search.append(('name', 'ilike', name))

        if description != None:
            search.append(('description', 'ilike', description))

        if vehicle != None:
            products = request.env['fleet.vehicle.model'].sudo().search_read([('id','=',vehicle)], fields=['x_product_ids'])[0]['x_product_ids']

            search.append(('id','in',products))

        res = request.env['product.product'].sudo().search_read(search, fields=fields)

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