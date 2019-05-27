from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from itertools import groupby


class BoardMekanikAPI(http.Controller):
    @http.route('/simontir/board-mekanik', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def boardMekanik(self, day, month, year):
        mekanik = request.env['hr.job'].sudo().search_read(
            [('name', '=', 'Mekanik')], fields=['id'])
        users_mekanik = request.env['hr.employee'].sudo(
        ).search([('job_id', '=', mekanik[0]['id'])])
        users = []

        domain = [('date_order', '=', '{}-{}-{}'.format(year, month, day))]

        for user in users_mekanik:
            domain_mekanik = ('mekanik_id', '=', user['user_id'][0]['user_id'])
            sales = request.env['sale.order'].sudo().search_count(domain)

            domain.append(domain_mekanik)

            today = request.env['sale.order'].sudo().search_count(domain)

            users.append({
                'name': user['name'],
                'total': sales,
                'today': today
            })

        return valid_response(status=200, data={
            'results': sorted(users, key=lambda s: s['total'], reverse=True)
        })
