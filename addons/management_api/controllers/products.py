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
    def productSearch(self, barcode=None, name=None, description=None, type=None, vehicle=None, page=0, register=None, equal='ilike', company_id=None):
        try:
            res = []

            search = []

            fields = ['name', 'barcode', 'qty_available',
                      'list_price', 'type', 'sales_count', 'product_tmpl_id', 'minimal_km']

            limit = 10
            offset = int(page)
            offset = ((offset - 1) if offset > 0 else 0) * limit

            if type != None:
                search.append(('type', '=', type))

            if barcode != None:
                search.append(('barcode', equal, barcode))

            if name != None:
                search.append(('name', equal, name))

            if description != None:
                search.append(('description', equal, description))

            if register != None:
                if register == 'true':
                    search.append(('registrasi', '=', True))

            if vehicle != None:
                products = request.env['fleet.vehicle.model'].sudo().search([
                    ('id', '=', vehicle)
                ])[0]['x_product_ids']

                arr = []
                
                if name != None and equal == "=":
                    for p in products:
                        if p.name.upper().replace(" ", "") == name.upper().replace(" ", ""):
                            arr.append(p.id)
                else:
                    arr = [p.id for p in products]

                search.append(('product_tmpl_id', 'in', arr))

            res = request.env['product.product'].sudo().search_read(
                search, fields=fields, limit=limit, offset=offset, order="sales_count desc")
            total = request.env['product.product'].sudo().search_count(search)

            if total <= 0:
                del search[-1]
                res = request.env['product.product'].sudo().search_read(
                    search, fields=fields, limit=limit, offset=offset, order="sales_count desc")
                total = request.env['product.product'].sudo(
                ).search_count(search)

            return valid_response(status=200, data={
                'count': total,
                'results': res
            })
        except Exception as identifier:
            print(traceback.format_exc())

    @http.route('/simontir/nopol/search', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def nopolSearch(self, nopol=None, company_id=None):
        res = []

        res = request.env['fleet.vehicle'].sudo().search_read([
            ('license_plate', 'ilike', nopol)
        ], fields=['license_plate'], limit=10)

        return valid_response(status=200, data={
            'count': len(res),
            'results': res
        })
