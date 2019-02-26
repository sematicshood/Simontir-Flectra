from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from . google import *

class FileAPIBentar(http.Controller, Google):
    def __init__(self):
        return super().__init__()

    @http.route('/simontir/file/kontakUpload', type="http", methods=["GET", "OPTIONS"], auth="none", cors="*", csrf=False)
    def kontakUpload(self, **params):
        try:
            domain = []
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
                license = request.env['fleet.vehicle'].sudo().search_read([('driver_id','=',k['id'])], fields=["license_plate"])

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
                        "value": 865737563345,
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
    def waBlaster(self, **params):
        try:
            domain = []
            fields = ['name']
            data   = []

            kontak = request.env['res.partner'].sudo().search_read(domain=domain, fields=fields)

            for k in kontak:
                license = request.env['fleet.vehicle'].sudo().search_read([('driver_id','=',k['id'])], fields=["license_plate"])

                if len(license) > 0:
                    data.append({
                        'Check': 'FALSE',
                        'Name': k['name'] + ' ' + license[0]['license_plate'],
                        'Status': '',
                    })

            return valid_response(status=200, data={
                'count': len(data),
                'results': data
            })

        except Exception as identifier:
            print(traceback.format_exc())