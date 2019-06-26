from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from itertools import groupby


class ProfileMekanikAPI(http.Controller):
    @http.route('/simontir/profile/mekanik/<int:id>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getMekanik(self, id, month=None, year=None, company_id=None):
        if month and year:
            count = 0
            month = int(month)
            year = int(year)

            if month != 12:
                domain_month = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year, month + 1)),
                    ('company_id', '=', int(company_id))]
            else:
                domain_month = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year + 1, 1)),
                    ('company_id', '=', int(company_id))]

            domain_year = [('create_date', '>=', '{}-1-1'.format(
                year)), ('create_date', '<', '{}-1-1'.format(year + 1))]

        hr = request.env['hr.employee'].sudo().search([
            ('user_id', '=', id),
            ('company_id', '=', int(company_id))
        ])

        domain_attendance_month = domain_month.copy()
        domain_attendance_month.append(('employee_id', '=', hr[0].id))
        attendance = request.env['hr.attendance'].sudo(
        ).search_count(domain_attendance_month)

        domain_unit_entri_month = domain_month.copy()
        domain_unit_entri_month.append(('mekanik_id', '=', id))
        unit_entri_month = request.env['sale.order'].sudo(
        ).search(domain_unit_entri_month)

        jasa_month = 0

        for unit_month in unit_entri_month:
            for line in unit_month.order_line:
                if line[0]['is_service']:
                    jasa_month += 1

        domain_unit_entri_year = domain_year.copy()
        domain_unit_entri_year.append(('mekanik_id', '=', id))
        unit_entri_year = request.env['sale.order'].sudo(
        ).search(domain_unit_entri_month)

        jasa_year = 0

        for unit_year in unit_entri_year:
            for line in unit_year.order_line:
                if line[0]['is_service']:
                    jasa_year += 1

        unit_permonth = []
        unit_this_month = 0

        reguler_this_month = domain_year.copy()
        reguler_this_month.append(('x_antrian_service', '=', 'reguler'))
        reguler_this_month = request.env['sale.order'].sudo(
        ).search_count(reguler_this_month)

        booking_this_month = domain_year.copy()
        booking_this_month.append(
            ('x_antrian_service', '=', 'Booking Service'))
        booking_this_month = request.env['sale.order'].sudo(
        ).search_count(booking_this_month)

        domain_light_this_month = domain_year.copy()
        domain_light_this_month.append(
            ('x_antrian_service', '=', 'Light Repair'))
        light_this_month = request.env['sale.order'].sudo(
        ).search_count(domain_light_this_month)

        for x in range(1, 13):
            year = datetime.date.today().year
            count = 0
            if x != 12:
                domain_unit_permonth = [('date_order', '>=', '{}-{}-1'.format(
                    year, x)), ('date_order', '<', '{}-{}-1'.format(year, x + 1))]
            else:
                domain_unit_permonth = [('date_order', '>=', '{}-{}-1'.format(
                    year, x)), ('date_order', '<', '{}-{}-1'.format(year + 1, 1))]

            domain_unit_permonth.append(('mekanik_id', '=', id))

            rev = request.env['sale.order'].sudo().search(domain_unit_permonth)

            # if x == month:
            #     for r in rev:
            #         if r['x_antrian_service'] == 'Light Repair':
            #             light_this_month += 1
            #         if r['x_antrian_service'] == 'Booking Service':
            #             booking_this_month += 1
            #         if r['x_antrian_service'] == 'reguler':
            #             reguler_this_month += 1

            unit_permonth.append({
                'date': x,
                'unit_permonth': len(rev)
            })

        performance = len(unit_entri_month) / \
            attendance if attendance > 0 else 0

        return valid_response(status=200, data={
            'results': {
                'attendance': attendance,
                'unit_entri_month': len(unit_entri_month),
                'jasa_month': jasa_month,
                'performance': performance,
                'return_year': 0,
                'unit_entri_year': len(unit_entri_year),
                'jasa_year': jasa_year,
                'unit_permonth': unit_permonth,
                'unit_this_month': unit_this_month,
                'reguler_this_month': reguler_this_month,
                'light_this_month': light_this_month,
                'booking_this_month': booking_this_month
            }
        })
