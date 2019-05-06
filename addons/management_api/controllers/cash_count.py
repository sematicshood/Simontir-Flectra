from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from datetime import datetime, timedelta

class CashCount(http.Controller):

    @http.route('/simontir/cash_count', methods=["GET", "OPTIONS"], cors="*", csrf=False, auth="none", type="http")
    def getCashCount(self, date = None):
        try:
            domain = []

            if date != None:
                domain.append(('date', '=', date))

            data = request.env['cash.count'].sudo().search_read(domain)

            return valid_response(status=200, data={
                    'count': len(data),
                    'results': data
                })
        except Exception as identifier:
            print(traceback.format_exc())

    @http.route('/simontir/cash_count/get_total_saldo', methods=["GET", "OPTIONS"], cors="*", csrf=False, auth="none", type="http")
    def getTotalSaldo(self, date = None):
        try:
            domain = [('invoice_status', '=', 'invoiced')]

            if date != None:
                da    = datetime.strptime(date, '%Y-%m-%d')
                d     = da + timedelta(days=1)

                domain.append(('create_date', '>=', date))
                domain.append(('create_date', '<', d.strftime("%Y-%m-%d")))

            data = request.env['sale.order'].sudo().search_read(domain, fields=['amount_total'])

            total = 0

            for d in data:
                total += d['amount_total']

            return valid_response(status=200, data={
                    'results': total
                })
        except Exception as identifier:
            print(traceback.format_exc())

    @http.route('/simontir/cash_count', methods=["POST", "OPTIONS"], cors="*", csrf=False, auth="none", type="json")
    def createCashCount(self):
        try:
            data = request.jsonrequest
            cash = request.env['cash.count'].sudo()

            cek  = cash.search([('date', '=', data['date'])])

            if len(cek) > 0:
                cek.write(data)
            else:
                cash.create(data)
        except Exception as identifier:
            print(traceback.format_exc())