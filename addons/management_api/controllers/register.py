from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *

class RegisterAPIBentar(http.Controller):
    #RESPONSE
    # {
    #     "count": 1,
    #     "results": [
    #         {
    #             "id": 28,
    #             "name": "SO026"
    #         }
    #     ]
    # }
    @http.route('/simontir/cekso', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    @authentication
    def onLoad(self):
        try:
            #cek SO dengan state quotation
            cek = self.cekSO()
            if len(cek) == 0 :
                createSO = request.env['sale.order'].sudo().create({
                    'partner_id': 1
                    })
                cek = self.cekSO()
                
            data = [{
                "id": data.id,
                "name": data.name,
                "tipe_motor":[{
                    "id":d.id,
                    "name": d.display_name
                }for d in request.env['fleet.vehicle.model'].sudo().search([])]
            }for data in cek]

            return valid_response(status=200, data={
                'count': len(data),
                'results': data
                })
        except Exception as e:
            print(str(e))

    def cekSO(self):
        cek = request.env['sale.order'].sudo().search([
            ('state', '=', 'draft')
            ])
        return cek

    @http.route('/simontir/createRegister', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    @authentication
    def createRegister(self):
        print(request.jsonrequest)
        print('-'*100)
        pass

    @http.route('/simontir/ceknopol', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    #RESPONSE
    # {
    #     "count": 1,
    #     "results": [
    #         {
    #             "data": "Nopol Sudah Terdaftar",
    #             "id_fleet_vehicle": 256,
    #             "nopol": "AA 6015 VW",
    #             "no_mesin": "ISO 3841",
    #             "no_rangka": false,
    #             "tahun": false,
    #             "nama_pemilik": "ADIFA",
    #             "telp_pemilik": false,
    #             "email_pemilik": false,
    #             "sosmed": false,
    #             "history": [
    #                 {
    #                     "id": 13,
    #                     "tanggal": "2019-01-04",
    #                     "biaya": 30000,
    #                     "km": 0,
    #                     "frontdesk": "Administrator",
    #                     "mekanik": false,
    #                     "jasa": [],
    #                     "part": false
    #                 }
    #             ]
    #         }
    #     ]
    # }
    @authentication
    def cekNopol(self, nopol):
        try:
            cek = request.env['fleet.vehicle'].sudo().search([('license_plate', '=', nopol)])
            print(cek[0].log_services.cost_ids)
            if len(cek) == 0:
                data = [{
                    "data": "Nopol Belum Terdaftar"
                }]
            else:
                data = [{
                    "data": "Nopol Sudah Terdaftar",
                    "id_fleet_vehicle":d.id,
                    "nopol":d.license_plate,
                    "no_mesin": d.vin_sn,
                    "no_rangka": d.location,
                    "tahun": d.model_year,
                    "nama_pemilik": d.driver_id.name,
                    "telp_pemilik": d.driver_id.mobile,
                    "email_pemilik":d.driver_id.email,
                    "sosmed": d.driver_id.website,
                    "history": [{
                        "id": h.id,
                        "tanggal": h.date,
                        "biaya":h.amount,
                        "km": h.odometer,
                        "frontdesk": h.write_uid.name, 
                        "mekanik": h.x_mekanik.name,
                        "jasa": [{
                            "id":c.id,
                            "name": c.name
                        }for c in h.cost_ids],
                        "part": h.description
                    }for h in d.log_services]
                } for d in cek]
            return valid_response(status=200, data={
                'count': len(data),
                'results': data
                })
        except Exception as e:
            print(str(e))

    @http.route('/simontir/saran-part', type='http', auth='none', methods=['GET'], csrf=False, cors="*")
    @authentication
    def saranPart(self, id_type):
        try:
            print(id_type)
            xxx = request.env['product.product'].sudo().search([('id', '=', 3)])
            print(xxx)
            xxx.sudo().write({
                "x_type_motor": 1
            })
            part = request.env['product.product'].sudo().search([('x_type_motor.id', '=', id_type)])
            data = [{
                "id_product": d.id,
                "name": d.name,
                "type_motor": d.x_type_motor.id
            } for d in part]

            return valid_response(status=200, data={
                'count': len(data),
                'results': data
                })
        except Exception as e:
            print(str(e))

    @http.route('/simontir/save', type='http', auth='none', methods=['POST'], csrf=False, cors="*")
    @authentication
    def saveRegister(self, aaa):
        # a = request.httprequest.POST['aaa']
        print(aaa)
        return "AAAA"