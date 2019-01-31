from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime

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
                }for d in request.env['fleet.vehicle.model'].sudo().search([])],
                "product": [{
                    "id":p.id,
                    "name": p.name,
                    "product_type": p.type,
                    "harga": p.list_price,
                    "stok": p.qty_available
                }for p in request.env['product.product'].sudo().search([])]
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
        tgl = ((request.jsonrequest['tgl_service']).split("T")[0]+" 00:00:00")
        tgll = datetime.datetime.strptime(tgl, '%Y-%m-%d %H:%M:%S')
        print('-'*100)
        
        #cek no polisi
        cekNopol = request.env['fleet.vehicle'].sudo().search([("license_plate", "=", request.jsonrequest['no_polisi'])])
        if len(cekNopol) == 0:
            print("kosong")

            createPemilik = request.env['res.partner'].sudo().create({
                "name":request.jsonrequest['nama_pemilik'],
                "mobile":request.jsonrequest['no_telp'],
                "email":request.jsonrequest['email'],
                "website":request.jsonrequest['sosmed']
            })

            createPembawa = request.env['res.partner'].sudo().create({
                "parent_id": createPemilik.id,
                "name":request.jsonrequest['nama_pembawa'],
                "street":request.jsonrequest['alamat'],
                "type":"other"
            })

            createDataMotor = request.env['fleet.vehicle'].sudo().create({
                "license_plate":request.jsonrequest['no_polisi'],
                "vin_sn":request.jsonrequest['no_mesin'],
                "location":request.jsonrequest['no_rangka'],
                "model_id":request.jsonrequest['type_id'],
                "model_year":request.jsonrequest['tahun'],
                "driver_id": createPemilik.id
            })

            createSaleOrder = request.env['sale.order'].sudo().search([('name', '=', request.jsonrequest['no_urut'])])
            createSaleOrder.sudo().write({
                "state":"sent",
                "partner_id": createPemilik.id,
                "x_antrian_service": request.jsonrequest['jenis_service'],
                "date_order":tgll
            })

            createKM = request.env['fleet.vehicle.odometer'].sudo().create({
                "value":request.jsonrequest['km'],
                "vehicle_id": createDataMotor.id
            })

            # dalam perulangan
            for data in request.jsonrequest['keluhan_konsumen']:
                createKeluhan = request.env['temporary.keluhan'].sudo().create({
                    "x_ref_so":createSaleOrder.id,
                    "x_keluhan": data['nama']
                })
            
            for data in request.jsonrequest['spareparts_selected']:
                createSOLine = request.env['sale.order.line'].sudo().create({
                    "order_id": createSaleOrder.id,
                    "product_id":data['id'],
                    "product_uom_qty":data['qty'],
                    "price_unit":data['harga'],
                    'price_subtotal':data['harga']
                })

            for data in request.jsonrequest['services_selected']:
                createSOLine = request.env['sale.order.line'].sudo().create({
                    "order_id": createSaleOrder.id,
                    "product_id":data['id'],
                    "product_uom_qty":1,
                    "price_unit":data['harga'],
                    'price_subtotal':data['harga']
                })

            print(request.env['product.product'].sudo().search([('name', '=', 'Cuci Motor')]).list_price)

            if request.jsonrequest['cuci'] == "True":
                createSOLine = request.env['sale.order.line'].sudo().create({
                    "order_id": createSaleOrder.id,
                    "product_id":request.env['product.product'].sudo().search([('name', '=', 'Cuci Motor')]).id,
                    "product_uom_qty":1,
                    "price_unit":request.env['product.product'].sudo().search([('name', '=', 'Cuci Motor')]).list_price,
                    'price_subtotal':request.env['product.product'].sudo().search([('name', '=', 'Cuci Motor')]).list_price
                })
            
        else:
            print("ada")
            createPembawa = request.env['res.partner'].sudo().create({
                "parent_id": cekNopol.driver_id.id,
                "name":request.jsonrequest['nama_pembawa'],
                "street":request.jsonrequest['alamat'],
                "type":"other"
            })

            createSaleOrder = request.env['sale.order'].sudo().search([('name', '=', request.jsonrequest['no_urut'])])
            createSaleOrder.sudo().write({
                "state": "sent",
                "partner_id": cekNopol.driver_id.id,
                "x_antrian_service": request.jsonrequest['jenis_service'],
                "date_order":tgll
            })

            createKM = request.env['fleet.vehicle.odometer'].sudo().create({
                "value":request.jsonrequest['km'],
                "vehicle_id": cekNopol.id
            })

            # dalam perulangan
            for data in request.jsonrequest['keluhan_konsumen']:
                createKeluhan = request.env['temporary.keluhan'].sudo().create({
                    "x_ref_so":createSaleOrder.id,
                    "x_keluhan": data['nama']
                })
            
            for data in request.jsonrequest['spareparts_selected']:
                createSOLine = request.env['sale.order.line'].sudo().create({
                    "order_id": createSaleOrder.id,
                    "product_id":data['id'],
                    "product_uom_qty":data['qty'],
                    "price_unit":data['harga'],
                    'price_subtotal':data['harga']
                })

            for data in request.jsonrequest['services_selected']:
                createSOLine = request.env['sale.order.line'].sudo().create({
                    "order_id": createSaleOrder.id,
                    "product_id":data['id'],
                    "product_uom_qty":1,
                    "price_unit":data['harga'],
                    'price_subtotal':data['harga']
                })

            print(request.env['product.product'].sudo().search([('name', '=', 'Cuci Motor')]).list_price)

            if request.jsonrequest['cuci'] == "True":
                createSOLine = request.env['sale.order.line'].sudo().create({
                    "order_id": createSaleOrder.id,
                    "product_id":request.env['product.product'].sudo().search([('name', '=', 'Cuci Motor')]).id,
                    "product_uom_qty":1,
                    "price_unit":request.env['product.product'].sudo().search([('name', '=', 'Cuci Motor')]).list_price,
                    'price_subtotal':request.env['product.product'].sudo().search([('name', '=', 'Cuci Motor')]).list_price
                })
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
    def cekNopol(self, *args, **kwargs):
        try:
            cek = request.env['fleet.vehicle'].sudo().search([('license_plate', '=', request.params.get('nopol'))])
            # print(cek[0].log_services.cost_ids)
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

    # @http.route('/simontir/save', type='http', auth='none', methods=['POST'], csrf=False, cors="*")
    # @authentication
    # def saveRegister(self, aaa):
    #     # a = request.httprequest.POST['aaa']
    #     print(aaa)
    #     return "AAAA"