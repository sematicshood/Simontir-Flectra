from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class CashCount(http.Controller):

    @http.route('/simontir/cash_count', methods=["GET", "OPTIONS"], cors="*", csrf=False, auth="none", type="http")
    def getCashCount(self, date=None, company_id=None):
        try:
            domain = [('company_id', '=', int(company_id))]

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
    def getTotalSaldo(self, date=None, company_id=None):
        try:
            da = datetime.strptime(date, '%Y-%m-%d')
            d = da + timedelta(days=1)
            ma = datetime.strptime("{}-{}-{}".format(da.year, da.month, 1), '%Y-%m-%d')
            m = ma + relativedelta(month=da.month+1)

            domain = ['&', '&', ('date', '>=', date), ('date', '<', d.strftime("%Y-%m-%d")), '&', '&', ('date', '>=', ma), ('date', '<', m), ("state", "not in", ["draft", "cancel"]), '|', ("type", "=", "out_invoice"), ("type", "=", "out_refund"), ('company_id', '=', int(company_id))]

            data = request.env['account.invoice'].sudo().search_read(
                domain, fields=['amount_total'])

            total = 0

            for d in data:
                total += d['amount_total']

            return valid_response(status=200, data={
                'results': total,
                'data': data,
            })
        except Exception as identifier:
            print(traceback.format_exc())

    @http.route('/simontir/cash_count', methods=["POST", "OPTIONS"], cors="*", csrf=False, auth="none", type="json")
    def createCashCount(self, company_id):
        try:
            data = request.jsonrequest
            cash = request.env['cash.count'].sudo()

            cek = cash.search([
                ('date', '=', data['date']), ('company_id', '=', int(company_id))
            ])

            if len(cek) > 0:
                cek.write(data)
            else:
                cash.create(data)
        except Exception as identifier:
            print(traceback.format_exc())
