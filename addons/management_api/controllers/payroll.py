from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from itertools import groupby
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Payroll(http.Controller):
    def build_dict(self, seq, key):
        return dict((d[key].split(' ')[0], dict(d, index=index)) for (index, d) in enumerate(seq))

    def get_bonus(self, tp):
        nominal = 0

        if tp < 348:
            nominal = 1000
        elif tp < 464:
            nominal = 2500
        elif tp < 580:
            nominal = 3000
        else:
            nominal = 4000

        return round((tp/58) * nominal)

    @http.route('/simontir/payroll', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getMekanik(self, day = 1, month = None, year = None, day_until = 1, month_until = None, year_until = None, type = None, company_id=None):
        month = int(month)
        year = int(year)
        day = int(day)
        month_until = int(month_until)
        year_until = int(year_until)
        day_until = int(day_until)

        domain = []

        if type == 'harian':
            domain = [('check_in', '>=', '{}-{}-{}'.format(
                    year, month, day)), ('check_in', '<', str(datetime(year, month, day) + timedelta(days=1))),
                    ('company_id', '=', int(company_id))]

        if type == 'bulanan':
            domain = [('check_in', '>=', str(datetime(year, month, day))), ('check_in', '<', str(datetime(year, month, day) + relativedelta(months=1))),
            ('company_id', '=', int(company_id))]

        if type == 'range':
            domain = [('check_in', '>=', str(datetime(year, month, day))), ('check_in', '<', str(datetime(year_until, month_until, day_until))),
            ('company_id', '=', int(company_id))]

        mekanik = request.env['hr.job'].sudo().search_read([
            ('name', '=', 'Mekanik'),
            ('company_id', '=', int(company_id))
        ], fields=['id'])

        users_mekanik = request.env['hr.employee'].sudo().search([
            ('job_id', '=', mekanik[0]['id']),
            ('company_id', '=', int(company_id))
        ])

        data = []

        for u in users_mekanik:
            att = []
            domain.append(('employee_id', '=', u.id))
            attendance = request.env['hr.attendance'].sudo().search(domain)

            point = 0
            bonus = 0

            for o in attendance:
                get_order = self.build_dict(att, key="check_in")
                od = get_order.get(o.check_in.split(' ')[0])
                od_bonus_jasa = self.get_bonus(o.intensif_jasa)
                od_bonus_part = self.get_bonus(o.intensif_part)
                total_bonus = o.ins_cuci_motor + od_bonus_part + od_bonus_jasa

                if od is None:
                    att.append({
                        'check_in': o.check_in.split(' ')[0],
                        'point_jasa': o.intensif_jasa,
                        'bonus_jasa': od_bonus_jasa,
                        'point_part': o.intensif_part,
                        'bonus_part': od_bonus_part,
                        'cuci': o.ins_cuci_motor,
                        'total_bonus': total_bonus,
                        'total_ue': o.total_ue
                    })
                else:
                    att[od['index']] = {
                        'check_in': o.check_in.split(' ')[0],
                        'point_jasa': int(o.intensif_jasa) + int(od['point_jasa']),
                        'bonus_jasa': int(od['bonus_jasa']) + int(od_bonus_jasa),
                        'point_part': int(o.intensif_part) + int(od['point_part']),
                        'bonus_part': int(od['bonus_part']) + int(od_bonus_part),
                        'cuci': int(o.ins_cuci_motor) + int(od['cuci']),
                        'total_bonus': int(total_bonus) + int(od['total_bonus']),
                        'total_ue': int(o.total_ue) + int(od['total_ue'])
                    }

                point += o.intensif_jasa
                point += o.intensif_part
                point += o.ins_cuci_motor

                bonus += od_bonus_jasa
                bonus += od_bonus_part

            data.append({
                'nama': u.name,
                'point': point,
                'bonus': bonus,
                'data': att
            })

        return valid_response(status=200, data={
            'results': data
        })
