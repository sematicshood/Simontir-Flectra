from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback

class RegisterAPIBentar(http.Controller):
    def cekNotExist(self, order_id, product_id):
        count = request.env['sale.order.line'].sudo().search_count([('order_id','=',order_id), ('product_id','=',product_id)])

        if count > 0:
            return False
        else:
            return True

    def cekTempNotExist(self, ref):
        count = request.env['temporary.analisa'].sudo().search_count([('x_ref_so','=',ref)])

        if count > 0:
            return False
        else:
            return True

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
    # @authentication

    # RESPONSE
    # {
    # "count": 1,
    # "results":[
    #     {
    #     "id": 46,
    #     "name": "SO044",
    #     "tipe_motor":[],
    #     "product":[
    #         {
    #         "id": 42,
    #         "name": "Ice Cream",
    #         "product_type": "product",
    #         "harga": 100,
    #         "stok": 0,
    #         "product_code": "ABCDE123",
    #         "similiar": "Es Dung Dung"
    #         }
    #     ],
    # "colors":[]
    # }
    def onLoad(self):
        try:
            #cek SO dengan state quotation
            cek = self.cekSO()
            if len(cek) == 0 :
                createSO = request.env['sale.order'].sudo().create({
                    'partner_id': 1
                    })
                cek = self.cekSO()

            brand   =   request.env['fleet.vehicle.model.brand'].sudo().search([('name','ilike','Honda')]);
                
            data = [{
                "id": data.id,
                "name": data.name,
                "tipe_motor":[{
                    "id":d.id,
                    "name": d.display_name
                }for d in request.env['fleet.vehicle.model'].sudo().search([('brand_id','=',brand[0].id)])],
                "product": [{
                    "id":p.id,
                    "name": p.name,
                    "product_type": p.type,
                    "harga": p.list_price,
                    "stok": p.qty_available,
                    "product_code": p.barcode,
                    "similiar": p.description
                }for p in request.env['product.product'].sudo().search([])]
            }for data in cek]

            colors = [{
                "color": color.color
            } for color in request.env['vehicle.colors'].sudo().search([])]

            return valid_response(status=200, data={
                'count': len(data),
                'results': data,
                'colors': colors,
                })
        except Exception as e:
            print(str(e))

    def cekSO(self):
        cek = request.env['sale.order'].sudo().search([
            ('state', '=', 'draft')
            ])
        return cek

    @http.route('/simontir/createRegister', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def createRegister(self):
        # cekSo = request.env['sale.order'].sudo().search()[('name', '=', request.jsonrequest['noUrut'])]
        # if cekSo.state == "sent":
        #     print(cekSo.state)
        #     print("sudah save")
        #     pass
        print(request.jsonrequest)

        cekColorExist   =   request.env['vehicle.colors'].sudo().search_count([('color','=',request.jsonrequest['warnaKendaraan'])])

        if cekColorExist == 0:
            request.env['vehicle.colors'].sudo().create({
                'color': request.jsonrequest['warnaKendaraan']
            })

        try:
            tgl = ((request.jsonrequest['tglService']).split("T")[0]+" 00:00:00")
            tgll = datetime.datetime.strptime(tgl, '%Y-%m-%d %H:%M:%S')

            cekNopol = request.env['fleet.vehicle'].sudo().search([("license_plate", "=", request.jsonrequest['noPolisi'])])
            if len(cekNopol) == 0:
                print("kosong")

                createPemilik = request.env['res.partner'].sudo().create({
                    "name":"" if 'namaPemilik' not in request.jsonrequest else request.jsonrequest['namaPemilik'],
                    "mobile":"" if 'noTelp' not in request.jsonrequest else request.jsonrequest['noTelp'],
                    "email":"" if 'email' not in request.jsonrequest else request.jsonrequest['email'],
                    "website":"" if 'sosmed' not in request.jsonrequest else request.jsonrequest['sosmed']
                })

                createPembawa = request.env['res.partner'].sudo().create({
                    "parent_id": createPemilik.id,
                    "name":"" if 'namaPembawa' not in request.jsonrequest else request.jsonrequest['namaPembawa'],
                    "street":"" if 'alamat' not in request.jsonrequest else request.jsonrequest['alamat'],
                    "type":"other"
                })

                createDataMotor = request.env['fleet.vehicle'].sudo().create({
                    "license_plate":"" if 'noPolisi' not in request.jsonrequest else request.jsonrequest['noPolisi'],
                    "vin_sn":"" if 'noMesin' not in request.jsonrequest else request.jsonrequest['noMesin'],
                    "location":"" if 'noRangka' not in request.jsonrequest else request.jsonrequest['noRangka'],
                    "model_id":"" if len(request.jsonrequest['type']) == 0 else request.jsonrequest['type']['id'],
                    "model_year":"" if 'tahun' not in request.jsonrequest else request.jsonrequest['tahun'],
                    "driver_id": createPemilik.id,
                    "color": request.jsonrequest['warnaKendaraan'],
                })

                createSaleOrder = request.env['sale.order'].sudo().search([('name', '=', request.jsonrequest['noUrut'])])
                createSaleOrder.sudo().write({
                    "state":"sent",
                    "partner_id": createPemilik.id,
                    "partner_invoice_id":createPemilik.id,
                    "partner_shipping_id": createPemilik.id,
                    "x_antrian_service": "" if 'jenisService' not in request.jsonrequest else request.jsonrequest['jenisService'],
                    "x_is_wash": True if request.jsonrequest['cuci'] == "true" else False,
                    "x_nopol": "" if 'noPolisi' not in request.jsonrequest else request.jsonrequest['noPolisi'],
                    "x_type_motor": "" if len(request.jsonrequest['type']) == 0 else request.jsonrequest['type']['name'],
                    "date_order":tgll,
                    "gross_amount": "" if 'total' not in request.jsonrequest else request.jsonrequest['total'],
                    "x_kpb": request.jsonrequest['kpb'],
                    "x_service": request.jsonrequest['service'],
                    "x_turun_mesin": request.jsonrequest['turunMesin'],
                    "x_ganti_oli": request.jsonrequest['gantiOli'],
                    "x_ganti_part": request.jsonrequest['gantiPart'],
                })

                createKM = request.env['fleet.vehicle.odometer'].sudo().create({
                    "value":"" if 'km' not in request.jsonrequest else request.jsonrequest['km'],
                    "vehicle_id": createDataMotor.id
                })

                # dalam perulangan
                for data in request.jsonrequest['keluhanKonsumen']:
                    createKeluhan = request.env['temporary.keluhan'].sudo().create({
                        "x_ref_so":createSaleOrder.id,
                        "x_keluhan": "" if 'nama' not in data else data['nama']
                    })

                if self.cekTempNotExist(createSaleOrder.id):
                    createAnalisa = request.env['temporary.analisa'].sudo().create({
                        "x_ref_so":createSaleOrder.id,
                        "x_analisa": "" if 'analisaService' not in request.jsonrequest else request.jsonrequest['analisaService'],
                        "x_saran": "" if 'analisaService' not in request.jsonrequest else request.jsonrequest['saranMekanik']
                    })
                else:
                    createAnalisa = request.env['temporary.analisa'].sudo().search([('x_ref_so','=',createSaleOrder.id)]).write({
                        "x_ref_so":createSaleOrder.id,
                        "x_analisa": "" if 'analisaService' not in request.jsonrequest else request.jsonrequest['analisaService'],
                        "x_saran": "" if 'analisaService' not in request.jsonrequest else request.jsonrequest['saranMekanik']
                    })
                
                product_id = []

                for data in request.jsonrequest['sparepartsSelected']:
                    product_id.append(data['id'])
                    if self.cekNotExist(createSaleOrder.id, data['id']):
                        createSOLine = request.env['sale.order.line'].sudo().create({
                            "order_id": createSaleOrder.id,
                            "product_id":"" if 'id' not in data else data['id'],
                            "name": "" if 'name' not in data else data['name'],
                            "product_uom_qty":"" if 'qty' not in data else data['qty'],
                            "price_unit":"" if 'harga' not in data else data['harga'],
                            'price_subtotal':"" if 'harga' not in data else data['harga']
                        })

                for data in request.jsonrequest['servicesSelected']:
                    product_id.append(data['id'])
                    if self.cekNotExist(createSaleOrder.id, data['id']):
                        createSOLine = request.env['sale.order.line'].sudo().create({
                            "order_id": createSaleOrder.id,
                            "product_id":"" if 'id' not in data else data['id'],
                            "name": "" if 'name' not in data else data['name'],
                            "product_uom_qty":1,
                            "price_unit":"" if 'harga' not in data else data['harga'],
                            'price_subtotal':"" if 'harga' not in data else data['harga']
                        })

                request.env['product.template'].sudo().search([('product_id','in',product_id)]).write({
                    'vehicle_models_ids': [(4,request.jsonrequest['type']['id'])]
                })

                notExist = request.env['sale.order.line'].sudo().search([
                    ('order_id','=',createSaleOrder.id),
                    ('product_id', 'not in', product_id)
                ])

                notExist.unlink()

                if request.jsonrequest['cuci'] == "true":
                    cuci = request.env['product.product'].sudo().search([('name', '=', 'CUCI MOTOR GRATIS')])

                    if self.cekNotExist(createSaleOrder.id, cuci.id):
                        createSOLine = request.env['sale.order.line'].sudo().create({
                            "order_id": createSaleOrder.id,
                            "product_id":cuci.id,
                            "name": 'CUCI MOTOR GRATIS',
                            "product_uom_qty":1,
                            "price_unit":cuci.list_price,
                            'price_subtotal':cuci.list_price
                        })
                
            else:
                print("ada")
                createPembawa = request.env['res.partner'].sudo().create({
                    "parent_id": cekNopol.driver_id.id,
                    "name":"" if 'namaPembawa' not in request.jsonrequest else request.jsonrequest['namaPembawa'],
                    "street":"" if 'alamat' not in request.jsonrequest else request.jsonrequest['alamat'],
                    "type":"other"
                })

                print(request.jsonrequest['gantiPart'])

                createSaleOrder = request.env['sale.order'].sudo().search([('name', '=', request.jsonrequest['noUrut'])])
                createSaleOrder.sudo().write({
                    "state":"sent",
                    "partner_id": cekNopol.driver_id.id,
                    "partner_invoice_id":cekNopol.driver_id.id,
                    "partner_shipping_id": cekNopol.driver_id.id,
                    "x_antrian_service": "" if 'jenisService' not in request.jsonrequest else request.jsonrequest['jenisService'],
                    "x_is_wash": True if request.jsonrequest['cuci'] == "true" else False,
                    "x_nopol": "" if 'noPolisi' not in request.jsonrequest else request.jsonrequest['noPolisi'],
                    "x_type_motor": "" if len(request.jsonrequest['type']) == 0 else request.jsonrequest['type']['name'],
                    "date_order":tgll,
                    "gross_amount": "" if 'total' not in request.jsonrequest else request.jsonrequest['total'],
                    "x_kpb": request.jsonrequest['kpb'],
                    "x_service": request.jsonrequest['service'],
                    "x_turun_mesin": request.jsonrequest['turunMesin'],
                    "x_ganti_oli": request.jsonrequest['gantiOli'],
                    "x_ganti_part": request.jsonrequest['gantiPart'],
                })

                createKM = request.env['fleet.vehicle.odometer'].sudo().create({
                    "value":"" if 'km' not in request.jsonrequest else request.jsonrequest['km'],
                    "vehicle_id": cekNopol.id
                })

                # dalam perulangan
                for data in request.jsonrequest['keluhanKonsumen']:
                    createKeluhan = request.env['temporary.keluhan'].sudo().create({
                        "x_ref_so":createSaleOrder.id,
                        "x_keluhan": "" if 'nama' not in data else data['nama']
                    })
                
                if self.cekTempNotExist(createSaleOrder.id):
                    createAnalisa = request.env['temporary.analisa'].sudo().create({
                        "x_ref_so":createSaleOrder.id,
                        "x_analisa": "" if 'analisaService' not in request.jsonrequest else request.jsonrequest['analisaService'],
                        "x_saran": "" if 'analisaService' not in request.jsonrequest else request.jsonrequest['saranMekanik']
                    })
                else:
                    createAnalisa = request.env['temporary.analisa'].sudo().search([('x_ref_so','=',createSaleOrder.id)]).write({
                        "x_ref_so":createSaleOrder.id,
                        "x_analisa": "" if 'analisaService' not in request.jsonrequest else request.jsonrequest['analisaService'],
                        "x_saran": "" if 'analisaService' not in request.jsonrequest else request.jsonrequest['saranMekanik']
                    })

                product_id = []

                for data in request.jsonrequest['sparepartsSelected']:
                    product_id.append(data['id'])
                    if self.cekNotExist(createSaleOrder.id, data['id']):
                        print(data['name'], data['id'], createSaleOrder.id)
                        createSOLine = request.env['sale.order.line'].sudo().create({
                            "order_id": createSaleOrder.id,
                            "product_id":"" if 'id' not in data else data['id'],
                            "name": "" if 'name' not in data else data['name'],
                            "product_uom_qty":"" if 'qty' not in data else data['qty'],
                            "price_unit":"" if 'harga' not in data else data['harga'],
                            'price_subtotal':"" if 'harga' not in data else data['harga']
                        })

                for data in request.jsonrequest['servicesSelected']:
                    product_id.append(data['id'])
                    if self.cekNotExist(createSaleOrder.id, data['id']):
                        print(data['name'], data['id'], createSaleOrder.id)
                        createSOLine = request.env['sale.order.line'].sudo().create({
                            "order_id": createSaleOrder.id,
                            "product_id":"" if 'id' not in data else data['id'],
                            "name": "" if 'name' not in data else data['name'],
                            "product_uom_qty":1,
                            "price_unit":"" if 'harga' not in data else data['harga'],
                            'price_subtotal':"" if 'harga' not in data else data['harga']
                        })

                if request.jsonrequest['cuci'] == "true":
                    cuci = request.env['product.product'].sudo().search([('name', '=', 'CUCI MOTOR GRATIS')])

                    if self.cekNotExist(createSaleOrder.id, cuci.id):
                        createSOLine = request.env['sale.order.line'].sudo().create({
                            "order_id": createSaleOrder.id,
                            "product_id":cuci.id,
                            "name": "CUCI MOTOR GRATIS",
                            "product_uom_qty":1,
                            "price_unit":cuci.list_price,
                            'price_subtotal':cuci.list_price
                        })

                request.env['product.template'].sudo().search([('product_id','in',product_id)]).write({
                    'vehicle_models_ids': [(4,request.jsonrequest['type']['id'])]
                })

                notExist = request.env['sale.order.line'].sudo().search([
                    ('order_id','=',createSaleOrder.id),
                    ('product_id', 'not in', product_id)
                ])

                notExist.unlink()
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())

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
    # @authentication
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
                    "tipe_motor":{
                        "id":d.model_id.id,
                        "name": d.model_id.display_name
                    },
                    "history": [{
                        "id": h.id,
                        "tanggal": h.date,
                        "biaya":h.amount,
                        "km": h.odometer,
                        "frontdesk": h.x_front_desk[0].name, 
                        "mekanik": h.x_mekanik[0].name,
                        "jasa": [{
                            "id":c.id,
                            "description": c.description
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
    # @authentication
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

    @http.route('/simontir/print-so/<path:so>', type='http', auth='none', methods=['GET'], csrf=False, cors="*")
    # @authentication
    def printSO(self, so):
        try:
            data = [{
                "id":d.id,
                "no_urut": so,
                "antrian_service": d.x_antrian_service,
                "tgl_service": d.date_order,
                "estimasi_waktu": d.x_estimasi_waktu,
                "is_wash": d.x_is_wash,
                "partner_id": d.partner_id.id,
                "nama_pemilik":d.partner_id.name,
                "no_telp": d.partner_id.mobile,
                "email": d.partner_id.email,
                "sosmed": d.partner_id.website,
                "nopol": d.x_nopol,
                "kpb": d.x_kpb,
                "service": d.x_service,
                "gantiOli": d.x_ganti_oli,
                "gantiPart": d.x_ganti_part,
                "turunMesin": d.x_turun_mesin,
                "pembawa":[{
                    "id":p.id,
                    "nama":p.name,
                    "alamat": p.street,
                    "type": p.type
                }for p in request.env['res.partner'].sudo().search([('parent_id', '=', d.partner_id.id)], order="id desc", limit=1)],
                "motor": [{
                    "id":m.id,
                    "no_polisi": m.license_plate,
                    "no_mesin":m.vin_sn,
                    "no_rangka":m.location,
                    "type": {
                        "id": m.model_id.id,
                        "name": m.model_id.name
                    },
                    "tahun": m.model_year,
                    "km": request.env['fleet.vehicle.odometer'].sudo().search([('vehicle_id', '=', m.id)], order="id desc", limit=1).value 
                }for m in request.env['fleet.vehicle'].sudo().search([('driver_id', '=', d.partner_id.id)])],
                "keluhan_konsumen": [{
                    "nama": k.x_keluhan
                }for k in request.env['temporary.keluhan'].sudo().search([('x_ref_so', '=', d.id)])],
                "analisa_service":request.env['temporary.analisa'].sudo().search([('x_ref_so', '=', d.id)]).x_analisa,
                "saran_mekanik":request.env['temporary.analisa'].sudo().search([('x_ref_so', '=', d.id)]).x_saran,
                "sale_order_line":[{
                    "id":s.product_id.id,
                    "name":s.product_id.name,
                    "type":s.product_id.type,
                    "qty":s.product_uom_qty,
                    "harga":s.price_unit,
                    "subtotal":s.price_subtotal
                }for s in request.env['sale.order.line'].sudo().search([('order_id', '=', d.id)])],
                "total": d.gross_amount
            }for d in request.env['sale.order'].sudo().search([('name', '=', so)])]

            print(data)

            return valid_response(status=200, data={
                'count': len(data),
                'results': data
                })
        except Exception as e:
            print(str(e))