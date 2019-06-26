from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from . google import *
from datetime import timedelta, datetime
import ast

class FileAPIBentar(http.Controller, Google):
    def __init__(self):
        return super().__init__()

    @http.route('/simontir/file/kontakUpload', type="http", methods=["GET", "OPTIONS"], auth="none", cors="*", csrf=False)
    def kontakUpload(self, company_id, **params):
        try:
            domain = [('company_id', '=', int(company_id))]
            fields = ['name', 'phone', 'email']
            data   = []
        
            if 'date' in params:
                spl         =   params['date'].split(' - ')
                fromDate    =   spl[0]
                untilDate   =   spl[1]

                domain.append(('create_date', '>=', fromDate))
                domain.append(('create_date', '<=', untilDate))

            if 'status' in params:
                if params['status'] != 'all':
                    domain.append(('is_sync', '=', False))    
            else:
                domain.append(('is_sync', '=', False))

            if 'idTest' in params:
                domain.append(('id', '=', 1))
            else:
                domain.append(('customer', '=', 'TRUE'))

            kontak = request.env['res.partner'].sudo().search_read(domain=domain, fields=fields)

            for k in kontak:
                license = request.env['fleet.vehicle'].sudo().search_read([
                    ('driver_id','=',k['id']),
                    ('company_id', '=', int(company_id))
                ], fields=["license_plate"])

                if len(license) > 0:
                    data.append({
                        "names": [
                            {
                                "givenName": k['name'],
                                "middleName": license[0]['license_plate']
                            }
                        ],
                        "phoneNumbers": [
                            {
                                "value": k['phone'],
                                "type": "Mobile"
                            }
                        ],
                        "emailAddresses": [
                            {
                                "value": k['email']
                            }
                        ]
                    })

            for d in data:
                self.createContact(d)

            payload = {
                "names": [
                    {
                        "givenName": "k['name']",
                        "middleName": "license[0]['license_plate']"
                    }
                ],
                "phoneNumbers": [
                    {
                        "value": "865737563345",
                        "type": "Mobile"
                    }
                ],
                "emailAddresses": [
                    {
                        "value": "k['email']"
                    }
                ]
            }

            self.createContact(payload)

            return valid_response(status=200, data={
                'count': len(data),
                'results': data
            })

        except Exception as identifier:
            print(traceback.format_exc())

    @http.route('/simontir/file/waBlaster', type="http", methods=["GET", "OPTIONS"], auth="none", cors="*", csrf=False)
    def waBlaster(self, company_id, **params):
        try:
            domain = [('company_id', '=', int(company_id))]
            fields = ['name', 'partner_id', 'x_nopol']
            data   = []

            if 'followUp' in params:
                if params['followUp'] == 'true':
                    today = datetime.today()
                    d     = today - timedelta(days=1)

                    domain.append(('create_date', '>=', d.strftime("%Y-%m-%d")))
                    domain.append(('create_date', '<', today.strftime("%Y-%m-%d")))

            if 'reminder' in params:
                if params['reminder'] == 'true':
                    today = datetime.today()
                    d     = today - timedelta(days=60)
                    nd    = d + timedelta(days=1)

                    domain.append(('create_date', '>=', d.strftime("%Y-%m-%d")))
                    domain.append(('create_date', '<', nd.strftime("%Y-%m-%d")))

            if 'date' in params:
                if params['date'] != '':
                    date  = params['date'].split(' - ')
                    start = date[0]
                    end   = date[1]

                    if start == end:
                        d = datetime.strptime(end, '%Y-%m-%d')

                        domain.append(('create_date', '>=', start))
                        domain.append(('create_date', '<', (d + timedelta(days=1)).strftime("%Y-%m-%d")))
                    else:
                        domain.append(('create_date', '>=', start))
                        domain.append(('create_date', '<=', end))

            if 'kpb' in params:
                kpb = params['kpb']
                if kpb != '':
                    domain.append(('x_kpb','=',int(kpb)))

            if 'service' in params:
                service = params['service']
                if service != '':
                    domain.append(('x_service','=',service))

            if 'ganti_oli' in params:
                ganti_oli = params['ganti_oli']
                if ganti_oli != 'false':
                    domain.append(('x_ganti_oli','=',True))

            if 'ganti_part' in params:
                ganti_part = params['ganti_part']
                if ganti_part != 'false':
                    domain.append(('x_ganti_part','=',True))

            if 'turun_mesin' in params:
                turun_mesin = params['turun_mesin']
                if turun_mesin != 'false':
                    domain.append(('x_turun_mesin','=',True))

            if 'type_motor' in params:
                type_motor = ast.literal_eval(params['type_motor'])
                if len(type_motor) > 0 and type_motor != 'null':
                    domain.append(('x_type_motor','in',type_motor))


            print(domain)

            sales = request.env['sale.order'].sudo().search_read(domain=domain, fields=fields)
            i = 1

            for s in sales:

                if s['x_nopol']:
                    data.append({
                        'No': i,
                        'Check': 'FALSE',
                        'Target': s['partner_id'][1] + ' ' + s['x_nopol'],
                        'Source': '',
                        'Status': '',
                    })

                    i += 1

            return valid_response(status=200, data={
                'count': len(data),
                'results': data
            })

        except Exception as identifier:
            print(traceback.format_exc())


    @http.route('/simontir/kendaraan/getType', type="http", methods=["GET", "OPTIONS"], auth="none", cors="*", csrf=False)
    def getTypeKendaraan(self, company_id, **params):
        try:
            brand   =   request.env['fleet.vehicle.model.brand'].sudo().search([
                ('name','ilike','Honda'),
                ('company_id', '=', int(company_id))
            ])

            type_motor =[d.display_name for d in request.env['fleet.vehicle.model'].sudo().search([
                ('brand_id','=',brand[0].id),
                ('company_id', '=', int(company_id))
            ])]

            return valid_response(status=200, data={
                'count': len(type_motor),
                'results': type_motor
            })

        except Exception as identifier:
            print(traceback.format_exc())