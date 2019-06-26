from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
from datetime import datetime, timedelta
import traceback

class UsersAPIBentar(http.Controller):
    def build_dict(self, seq, key):
        return dict((d[key].split(' ')[0], dict(d, index=index)) for (index, d) in enumerate(seq))

    def build_dict_day(self, seq, key):
        return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))

    @http.route('/simontir/unit_entri/month', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def unitEntriMonth(self, month, year, user_id, type, company_id):
        month = int(month)
        year = int(year)

        if month != 12:
            domain = [('date_order', '>=', '{}-{}-1'.format(
                year, month)), ('date_order', '<', '{}-{}-1'.format(year, month + 1)), ('company_id', '=', int(company_id))]
        else:
            domain = [('date_order', '>=', '{}-{}-1'.format(
                year, month)), ('date_order', '<', '{}-{}-1'.format(year + 1, 1)), ('company_id', '=', int(company_id))]

        role = "user_id"

        if type == 'mekanik':
            role = 'mekanik_id'
        elif type == 'staff':
            role = "user_id"
        elif type == 'finalcheck':
            role = "checker_id"

        domain.append((role, '=', int(user_id)))

        order = request.env['sale.order'].sudo().search(domain)

        data = []

        for o in order:
            get_order = self.build_dict(data, key="date_order")
            od = get_order.get(o.date_order.split(' ')[0])

            product = 0
            service = 0

            for line in o.order_line:
                if line.is_service:
                    service += 1
                else:
                    product += 1

            if od is None:
                data.append({
                    'date_order': o.date_order,
                    'total_order': 1,
                    'product': product,
                    'service': service,
                })
            else:
                data[od['index']] = {
                    'date_order': od['date_order'],
                    'total_order': int(od['total_order']) + 1,
                    'product': int(od['product']) + int(product),
                    'service': int(od['service']) + int(service),
                }

        return valid_response(status=200, data={
            'results': data
        })

    @http.route('/simontir/unit_entri/day', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def unitEntriDay(self, day, month, year, user_id, type, company_id):
        month = int(month)
        year = int(year)
        day = int(day)

        domain = [('date_order', '>=', '{}-{}-{}'.format(
                year, month, day)), ('date_order', '<', str(datetime(year, month, day) + timedelta(days=1))), ('company_id', '=', int(company_id))]

        role = ''

        if type == 'mekanik':
            role = 'mekanik_id'
        elif type == 'staff':
            role = "user_id"
        elif type == 'finalcheck':
            role = "checker_id"

        domain.append((role, '=', int(user_id)))

        order = request.env['sale.order'].sudo().search(domain)

        data = []

        for o in order:
            get_order = self.build_dict_day(data, key="x_nopol")
            od = get_order.get(o.x_nopol)

            if od is None:
                data.append({
                    'x_nopol': o.x_nopol,
                    'product': 0,
                    'service': 0,
                    'si': 0,
                    'cr': 0
                })
            else:
                product = 0
                service = 0
                si = 0
                cr = 0

                for line in o.order_line:
                    if line.is_service:
                        service += 1
                    else:
                        product += 1

                    if line.product_id.name.isupper() == 'Service injector'.isupper():
                        si += 1

                    if line.product_id.name.isupper() == 'Carbon remover'.isupper():
                        cr += 1

                data[od['index']] = {
                    'x_nopol': od['x_nopol'],
                    'product': int(od['product']) + int(product),
                    'service': int(od['service']) + int(service),
                    'si': int(od['si']) + int(si),
                    'cr': int(od['cr']) + int(cr),
                }

        return valid_response(status=200, data={
            'results': data
        })