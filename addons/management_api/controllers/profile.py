from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from itertools import groupby


class ProfileAPI(http.Controller):
    @http.route('/simontir/profile/owner/revenue', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def ownerRevenue(self, company_id):

        revenue = []

        for x in range(1, 13):
            year = datetime.date.today().year
            count = 0
            if x != 12:
                domain = [('date_order', '>=', '{}-{}-1'.format(
                    year, x)), ('date_order', '<', '{}-{}-1'.format(year, x + 1)),
                    ('company_id', '=', int(company_id))]
            else:
                domain = [('date_order', '>=', '{}-{}-1'.format(
                    year, x)), ('date_order', '<', '{}-{}-1'.format(year + 1, 1)),
                    ('company_id', '=', int(company_id))]

            rev = request.env['sale.order'].sudo().search_read(
                domain, fields=['amount_total'])

            for r in rev:
                count += r['amount_total']

            revenue.append({
                'date': '{}-{}'.format(x, year),
                'revenue': count
            })

        result = {
            'revenue': revenue,
        }

        return valid_response(status=200, data={
            'results': result
        })

    @http.route('/simontir/profile/owner/sales', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def ownerSales(self, month=None, year=None, company_id=None):

        sales = None

        if month and year:
            count = 0
            month = int(month)
            year = int(year)

            if month != 12:
                domain = [('date_order', '>=', '{}-{}-1'.format(
                    year, month)), ('date_order', '<', '{}-{}-1'.format(year, month + 1)),
                    ('company_id', '=', int(company_id))]
            else:
                domain = [('date_order', '>=', '{}-{}-1'.format(
                    year, month)), ('date_order', '<', '{}-{}-1'.format(year + 1, 1)),
                    ('company_id', '=', int(company_id))]

            sals = request.env['sale.order'].sudo().search_read(
                domain, fields=['amount_total'])

            for sale in sals:
                count += sale['amount_total']

            sales = count

        result = {
            'sales': sales
        }

        return valid_response(status=200, data={
            'results': result
        })

    @http.route('/simontir/profile/owner/product-revenue', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def productRevenue(self, month=None, year=None, company_id=None):

        service = []
        product = []

        if month and year:
            count = 0
            month = int(month)
            year = int(year)
            domain_service = [('is_service', '=', True), ('company_id', '=', int(company_id))]
            domain_product = [('is_service', '=', False), ('company_id', '=', int(company_id))]

            if month != 12:
                domain_from = ('create_date', '>=', '{}-{}-1'.format(
                    year, month))
                domain_to = ('create_date', '<',
                             '{}-{}-1'.format(year, month + 1))
            else:
                domain_from = ('create_date', '>=', '{}-{}-1'.format(
                    year, month))
                domain_to = ('create_date', '<', '{}-{}-1'.format(year + 1, 1))

            domain_service.append(domain_from)
            domain_service.append(domain_to)

            services = request.env['sale.order.line'].sudo(
            ).read_group(domain_service, ['product_id'], ['product_id'], lazy=False)

            for serv in services:
                service.append({
                    'name': serv['product_id'][1],
                    'product_id': serv['product_id'][0],
                    'sale': serv['__count']
                })

            domain_product.append(domain_from)
            domain_product.append(domain_to)

            products = request.env['sale.order.line'].sudo(
            ).read_group(domain_product, ['product_id'], ['product_id'], lazy=False)

            for prod in products:
                product.append({
                    'name': prod['product_id'][1],
                    'product_id': prod['product_id'][0],
                    'sale': prod['__count']
                })

        result = {
            'service': sorted(service, key=lambda s: s['sale'], reverse=True)[0:10],
            'product': sorted(product, key=lambda s: s['sale'], reverse=True)[0:10]
        }

        return valid_response(status=200, data={
            'results': result
        })

    @http.route('/simontir/profile/owner/new-return-customer', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def newReturnCustomer(self, month=None, year=None, company_id=None):

        returnCustomer = 0
        newCustomer = 0

        if month and year:
            count = 0
            month = int(month)
            year = int(year)

            if month != 12:
                domain = [('date_order', '>=', '{}-{}-1'.format(
                    year, month)), ('date_order', '<', '{}-{}-1'.format(year, month + 1)),
                    ('company_id', '=', int(company_id))]
            else:
                domain = [('date_order', '>=', '{}-{}-1'.format(
                    year, month)), ('date_order', '<', '{}-{}-1'.format(year + 1, 1)),
                    ('company_id', '=', int(company_id))]

            sales = request.env['sale.order'].sudo(
            ).read_group(domain, ['partner_id', 'amount_total'], ['partner_id'], lazy=False)

            for serv in sales:
                if serv['__count'] > 1:
                    returnCustomer += serv['amount_total']
                else:
                    newCustomer += serv['amount_total']

        result = {
            'newCustomer': newCustomer,
            'returnCustomer': returnCustomer
        }

        return valid_response(status=200, data={
            'results': result
        })

    @http.route('/simontir/profile/owner/rasio', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def rasio(self, month=None, year=None, company_id=None):
        unit_this_month = 0
        unit_previous_month = 0
        service_this_month = 0
        service_previous_month = 0
        attendance_this_month = 0
        attendance_previous_month = 0

        domain_attendance_this = []
        domain_attendance_prev = []

        if month and year:
            count = 0
            month = int(month)
            year = int(year)

            if month != 12:
                domain = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year, month + 1)),
                    ('company_id', '=', int(company_id))]
            else:
                domain = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year + 1, 1)),
                    ('company_id', '=', int(company_id))]

            if month != 1:
                prev_domain = [('create_date', '>=', '{}-{}-1'.format(
                    year, month - 1)), ('create_date', '<', '{}-{}-1'.format(year, month)),
                    ('company_id', '=', int(company_id))]
            else:
                prev_domain = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year - 1, 12)),
                    ('company_id', '=', int(company_id))]

            sales = request.env['sale.order.line'].sudo(
            ).search_read(domain, fields=['price_total', 'is_service'])
            sales_prev = request.env['sale.order.line'].sudo(
            ).search_read(prev_domain, fields=['price_total', 'is_service'])

            for sal in sales:
                unit_this_month += sal['price_total']

                if sal['is_service']:
                    service_this_month += sal['price_total']

            for sal in sales_prev:
                unit_previous_month += sal['price_total']

                if sal['is_service']:
                    service_previous_month += sal['price_total']

            mekanik = request.env['hr.job'].sudo().search_read([
                ('name', '=', 'Mekanik'),
                ('company_id', '=', int(company_id))
            ], fields=['id'])

            staff_mekanik = request.env['hr.employee'].sudo().search([
                ('job_id', '=', mekanik[0]['id']),
                ('company_id', '=', int(company_id))
            ])

            user_id = []

            for staff in staff_mekanik:
                user_id.append(staff.id)

            domain_attendance_this = domain
            domain_attendance_this.append(
                ('employee_id', 'in', user_id))

            domain_attendance_prev = prev_domain
            domain_attendance_prev.append(('employee_id', 'in', user_id))

            attendance_this_month = request.env['hr.attendance'].sudo(
            ).search_count(domain_attendance_this)
            attendance_previous_month = request.env['hr.attendance'].sudo(
            ).search_count(domain_attendance_prev)

        try:
            rasio_unit_this_month = unit_this_month / \
                len(staff_mekanik) / attendance_this_month
        except Exception as identifier:
            rasio_unit_this_month = 0

        try:
            rasio_unit_previous_month = unit_previous_month / \
                len(staff_mekanik) / attendance_previous_month
        except Exception as identifier:
            rasio_unit_previous_month = 0

        try:
            rasio_service_this_month = service_this_month / \
                len(staff_mekanik) / attendance_this_month
        except Exception as identifier:
            rasio_service_this_month = 0

        try:
            rasio_service_previous_month = service_previous_month / \
                len(staff_mekanik) / attendance_previous_month
        except Exception as identifier:
            rasio_service_previous_month = 0

        result = {
            'unit_this_month': unit_this_month,
            'unit_previous_month': unit_previous_month,
            'service_this_month': service_this_month,
            'service_previous_month': service_previous_month,
            'rasio_unit_this_month': rasio_unit_this_month,
            'rasio_unit_previous_month': rasio_unit_previous_month,
            'rasio_service_this_month': rasio_service_this_month,
            'rasio_service_previous_month': rasio_service_previous_month,
        }

        return valid_response(status=200, data={
            'results': result
        })

    @http.route('/simontir/profile/owner/staff-mekanik', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def staffMekanik(self, month=None, year=None, company_id=None):
        staff_users = []
        mekanik_users = []
        head_users = []
        part_this_month = 0
        total_this_month = 0

        if month and year:
            count = 0
            month = int(month)
            year = int(year)

            if month != 12:
                domain = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year, month + 1))]
            else:
                domain = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year + 1, 1))]

            mekanik = request.env['hr.job'].sudo().search_read([
                ('name', '=', 'Mekanik'),
                ('company_id', '=', int(company_id))
            ], fields=['id'])

            staff = request.env['hr.job'].sudo().search_read([
                ('name', '=', 'Staff'),
                ('company_id', '=', int(company_id))
            ], fields=['id'])

            jobs_select = request.env['hr.job'].sudo().search_read(
                ['|', ('name', '=', 'Kepala Mekanik'), ('name', '=', 'Kepala Bengkel'), ('company_id', '=', int(company_id))], fields=['id'])

            jobs = [job['id'] for job in jobs_select]

            staff_user = request.env['hr.employee'].sudo(
            ).search([
                ('job_id', '=', staff[0]['id']),
                ('company_id', '=', int(company_id))
            ])

            mekanik_user = request.env['hr.employee'].sudo(
            ).search([
                ('job_id', '=', mekanik[0]['id']),
                ('company_id', '=', int(company_id))
            ])

            head_user = request.env['hr.employee'].sudo(
            ).search([
                ('job_id', 'in', jobs),
                ('company_id', '=', int(company_id))
            ])

            domain_service = domain.copy()

            sales = request.env['sale.order.line'].sudo(
            ).search_read(domain_service, fields=['price_total', 'is_service'])

            for sal in sales:
                total_this_month += sal['price_total']

                if sal['is_service']:
                    part_this_month += sal['price_total']

            for staff in staff_user:
                domain_staff = domain.copy()
                domain_staff.append(('employee_id', '=', staff['id']))

                attendance = request.env['hr.attendance'].sudo(
                ).search_count(domain_staff)

                staff_users.append({
                    'name': staff['name'],
                    'attendance': attendance,
                    'omset': part_this_month,
                    'insentif': total_this_month,
                })

            for mekanik in mekanik_user:
                domain_mekanik = domain.copy()
                domain_mekanik.append(('employee_id', '=', mekanik['id']))
                domain_sale_mekanik = domain.copy()
                domain_sale_mekanik.append(
                    ('mekanik_id', '=', mekanik['user_id'][0]['id']))
                jasa = 0
                part = 0

                attendance = request.env['hr.attendance'].sudo(
                ).search_count(domain_mekanik)

                sales = request.env['sale.order'].sudo(
                ).search(domain_sale_mekanik)

                for sale in sales:
                    for line in sale['order_line']:
                        jasa += line['product_id'][0]['product_tmpl_id'][0]['x_ins_jasa']
                        part += line['product_id'][0]['product_tmpl_id'][0]['x_ins_part']

                mekanik_users.append({
                    'name': mekanik['name'],
                    'attendance': attendance,
                    'jasa': jasa,
                    'part': part,
                    'total': jasa + part
                })

            for head in head_user:
                domain_head = domain.copy()
                domain_head.append(('employee_id', '=', head['id']))

                attendance = request.env['hr.attendance'].sudo(
                ).search_count(domain_head)

                head_users.append({
                    'name': head['name'],
                    'attendance': attendance,
                    'omset_bengkel': total_this_month,
                    'omset_part': part_this_month,
                    'total': total_this_month + part_this_month
                })

        result = {
            'staff_users': staff_users,
            'mekanik_users': mekanik_users,
            'head_users': head_users
        }

        return valid_response(status=200, data={
            'results': result
        })

    @http.route('/simontir/profile/owner/service', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def service(self, month=None, year=None, company_id=None):
        booking_service_total_this_month = 0
        booking_service_total_prev_month = 0

        if month and year:
            count = 0
            month = int(month)
            year = int(year)

            if month != 12:
                domain = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year, month + 1)),
                    ('company_id', '=', int(company_id))]
            else:
                domain = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year + 1, 1)),
                    ('company_id', '=', int(company_id))]

            if month != 1:
                prev_domain = [('create_date', '>=', '{}-{}-1'.format(
                    year, month - 1)), ('create_date', '<', '{}-{}-1'.format(year, month)),
                    ('company_id', '=', int(company_id))]
            else:
                prev_domain = [('create_date', '>=', '{}-{}-1'.format(
                    year, month)), ('create_date', '<', '{}-{}-1'.format(year - 1, 12)),
                    ('company_id', '=', int(company_id))]

            domain.append(('x_antrian_service', '=', 'Booking Service'))
            prev_domain.append(('x_antrian_service', '=', 'Booking Service'))

            this_bookings = request.env['sale.order'].sudo(
            ).search_read(domain, fields=['gross_amount'])
            prev_bookings = request.env['sale.order'].sudo().search_read(
                prev_domain, fields=['gross_amount'])

            for booking in this_bookings:
                booking_service_total_this_month += booking['gross_amount']

            for booking in prev_bookings:
                booking_service_total_prev_month += booking['gross_amount']

        result = {
            'booking_service_total_this_month': booking_service_total_this_month,
            'booking_service_total_prev_month': booking_service_total_prev_month,
            'booking_service_unit_this_month': len(this_bookings),
            'booking_service_unit_prev_month': len(prev_bookings),
        }

        return valid_response(status=200, data={
            'results': result
        })
