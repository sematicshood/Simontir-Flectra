from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from itertools import groupby


class ProfileAPI(http.Controller):
    @http.route('/simontir/profile/staff/<int:id>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getStaff(self, id, month=None, year=None):
        if month and year:
            count = 0
            month = int(month)
            year = int(year)

            if month != 12:
                domain_attendance = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year, month + 1))]
                domain_unit_entri = [('date_order', '>=', '{}-{}-1'.format(
                    year, month)), ('date_order', '<', '{}-{}-1'.format(year, month + 1))]
            else:
                domain_attendance = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year + 1, 1))]
                domain_unit_entri = [('date_order', '>=', '{}-{}-1'.format(
                    year, month)), ('date_order', '<', '{}-{}-1'.format(year + 1, 1))]

        hr = request.env['hr.employee'].sudo().search([('user_id', '=', id)])

        domain_attendance.append(('employee_id', '=', hr[0].id))
        attendance = request.env['hr.attendance'].sudo(
        ).search_count(domain_attendance)

        domain_unit_entri.append(('write_uid', '=', id))
        unit_entri = request.env['sale.order'].sudo(
        ).search_count(domain_unit_entri)

        return valid_response(status=200, data={
            'results': {
                'attendance': attendance,
                'unit_entri': unit_entri
            }
        })
