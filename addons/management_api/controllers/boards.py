from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
from datetime import datetime, timedelta, date
import traceback


class BoardsAPIBentar(http.Controller):
    @http.route('/simontir/getso', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getso(self, company_id):
        try:
            so = request.env['sale.order'].sudo().search([
                ('invoice_status', '!=', 'invoiced'),
                ('state', '!=', 'cancel'),
                ('state', '!=', 'done'),
                ('company_id', '=', int(company_id))
            ], order="id desc")

            data = [{
                "no_polisi": s.x_nopol,
                "customer": s.partner_id[0].name,
                "tipe_kenadaraan": s.x_type_motor,
                "status": s.state,
                "invoice": s.invoice_status,
                "antrian_service": s.x_antrian_service,
                "date": s.date_order,
                "name": s.name,
                "cuci": s.x_is_wash,
                "mekanik": s.mekanik_id.name,
                "gross_amount": s.gross_amount,
                "order_line": [{
                    "name": o.name,
                    "type": o.product_id[0].product_tmpl_id[0].type
                } for o in s.order_line]
            } for s in so]

            return valid_response(status=200, data={
                'count': len(data),
                'results': data
            })
        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/getso_mekanik/<user_id>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getso_mekanik(self, user_id, company_id, date):
        try:
            date = date.split('-')

            partnerId = request.env['res.users'].sudo().search([
                ('id', '=', int(user_id)),
                ('company_id', '=', int(company_id))
            ])

            so = request.env['sale.order'].sudo().search([
                ('state', '=', 'sent'),
                ('company_id', '=', int(company_id)),
                ('date_order', '>=', '{}-{}-{}'.format(date[0], date[1], date[2])), 
                ('date_order', '<', str(datetime(int(date[0]), int(date[1]), int(date[2])) + timedelta(days=1)))
            ], order="id asc")

            owns = request.env['sale.order'].sudo().search([
                ('state', '=', 'sale'),
                ('invoice_status', '=', 'no'),
                ('mekanik_id', '=', int(user_id)),
                ('company_id', '=', int(company_id))
            ], order="id asc")

            data = [{
                "no_polisi": s.x_nopol,
                "customer": s.partner_id[0].name,
                "tipe_kenadaraan": s.x_type_motor,
                "status": s.state,
                "invoice": s.invoice_status,
                "antrian_service": s.x_antrian_service,
                "name": s.name,
                "cuci": s.x_is_wash,
                "order_line": [{
                    "name": o.name,
                    "type": o.product_id[0].product_tmpl_id[0].type
                } for o in s.order_line]
            } for s in so]

            own = [{
                "no_polisi": s.x_nopol,
                "customer": s.partner_id[0].name,
                "tipe_kenadaraan": s.x_type_motor,
                "status": s.state,
                "invoice": s.invoice_status,
                "antrian_service": s.x_antrian_service,
                "name": s.name,
                "cuci": s.x_is_wash,
                "order_line": [{
                    "name": o.name,
                    "type": o.product_id[0].product_tmpl_id[0].type
                } for o in s.order_line]
            } for s in owns]

            return valid_response(status=200, data={
                'count': len(data),
                'results': data,
                'own': own
            })
        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/getso_finalcheck', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getso_finalcheck(self, company_id, date):
        date = date.split('-')

        so = request.env['sale.order'].sudo().search([
            ('state', '=', 'done'), 
            ('invoice_status', '=', 'no'), 
            ('company_id', '=', int(company_id)),
            ('date_order', '>=', '{}-{}-{}'.format(date[0], date[1], date[2])), 
            ('date_order', '<', str(datetime(int(date[0]), int(date[1]), int(date[2])) + timedelta(days=1)))
        ], order="id asc")

        data = [{
            "no_polisi": s.x_nopol,
            "customer": s.partner_id[0].name,
            "tipe_kenadaraan": s.x_type_motor,
            "status": s.state,
            "invoice": s.invoice_status,
            "antrian_service": s.x_antrian_service,
            "name": s.name,
            "cuci": s.x_is_wash,
            "mekanik": s.mekanik_id.name,
            "order_line": [{
                "name": o.name,
                "type": o.product_id[0].product_tmpl_id[0].type
            } for o in s.order_line]
        } for s in so]

        return valid_response(status=200, data={
            'count': len(data),
            'results': data
        })

    @http.route('/simontir/pick_final', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def pick_final(self, company_id = False):
        try:
            rq = request.jsonrequest
            data = request.env['sale.order'].sudo().search([
                ('name', '=', rq['invoice']),
                ('company_id', '=', int(request.jsonrequest['company_id']))
            ])

            data.write({
                'invoice_status': 'no',
                'checker_id': rq['user_id'],
            })

        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/pick_so', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def pick_so(self, company_id = False):
        try:
            rq = request.jsonrequest
            
            data = request.env['sale.order'].sudo().search([
                ('name', '=', rq['invoice']),
                ('company_id', '=', int(request.jsonrequest['company_id']))
            ])

            if len(data[0]['mekanik_id']) == 0:
                day = date.today().day
                month = date.today().month
                year = date.today().year

                employee = request.env['hr.employee'].sudo().search([
                    ('user_id', '=', rq['user_id']),
                ])

                attendance = request.env['hr.attendance'].sudo().search([
                    ('employee_id', '=', employee[0]['id']), 
                    ('check_in', '>=', str((datetime.now()).date())), 
                    ('check_in', '<', str((datetime.now() + timedelta(days=1)).date())),
                ])

                if len(attendance) == 0:
                    return invalid_response(400, 'Bad Request', 'Absensi terlebih dahulu')

                attendance.write({
                    'total_ue': attendance.total_ue + 1,
                })

                data.action_confirm()

                data.write({
                    'invoice_status': 'no',
                    'mekanik_id': rq['user_id'],
                })

                so = request.env['account.analytic.account'].sudo().search_read([
                    ('name', 'like', rq['invoice']),
                ], fields=['project_ids'])

                request.env['sale.order'].sudo().search([
                    ('name', '=', rq['invoice']),
                    ('company_id', '=', int(request.jsonrequest['company_id']))
                ]).write({
                    'x_waktu_mulai': datetime.now()
                })
                print(so)

                tasks = request.env['project.task'].sudo().search([
                    ('project_id', '=', so[0]['project_ids'][0]),
                ])

                for order in data[0]['order_line']:
                    if order.product_id[0].product_tmpl_id[0].type != 'service':
                        request.env['project.task'].sudo().create({
                            'name': rq['invoice'] + ' sparepart:' + order.product_id[0].product_tmpl_id[0].name,
                            'user_id': rq['user_id'],
                            'company_id': tasks[0].company_id[0].id,
                            'email_from': tasks[0].email_from,
                            'priority': 'l',
                            'planned_hours': 1,
                            'project_id': so[0]['project_ids'][0],
                            'sale_line_id': order.id
                        })
                    if order.product_id[0].product_tmpl_id[0].name == 'CUCI MOTOR GRATIS':
                        request.env['project.task'].sudo().create({
                            'name': rq['invoice'] + ':CUCI MOTOR GRATIS',
                            'user_id': rq['user_id'],
                            'company_id': tasks[0].company_id[0].id,
                            'email_from': tasks[0].email_from,
                            'priority': 'l',
                            'planned_hours': 1,
                            'project_id': so[0]['project_ids'][0],
                            'sale_line_id': order.id
                        })

                for task in tasks:
                    task.write({
                        'user_id': rq['user_id']
                    })

                keluhan = request.env['temporary.keluhan'].sudo().search([
                    ('x_ref_so', '=', data[0]['id']),
                ])

                for kel in keluhan:
                    request.env['project.task'].sudo().create({
                        'name': rq['invoice'] + ' keluhan:' + kel.x_keluhan,
                        'user_id': rq['user_id'],
                        'company_id': tasks[0].company_id[0].id,
                        'email_from': tasks[0].email_from,
                        'priority': 'l',
                        'planned_hours': 1,
                        'task_seq': '',
                        'project_id': so[0]['project_ids'][0],
                        'sale_line_id': False
                    })

        except Exception as identifier:
            print(traceback.format_exc())
            print(identifier)

    @http.route('/simontir/get_final_detail/<path:no_ref>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def get_final_detail(self, no_ref, company_id):
        try:
            no_ref = str(no_ref)

            sale = request.env['sale.order'].sudo().search_read([
                ('name', '=', no_ref),
                ('company_id', '=', int(company_id))
            ], fields=['x_nopol', 'x_waktu_mulai', 'x_is_wash'])

            so = request.env['account.analytic.account'].sudo().search_read([
                ('name', 'like', no_ref),
            ], fields=['project_ids'])

            tasks = request.env['project.task'].sudo().search_read([
                ('project_id', '=', so[0]['project_ids'][0]),
            ], fields=['name', 'x_status'])

            return valid_response(status=200, data={
                'count': len(tasks),
                'results': {
                    'waktu_mulai': sale[0]['x_waktu_mulai'],
                    'nopol': sale[0]['x_nopol'],
                    'cuci': sale[0]['x_is_wash'],
                    'tasks': tasks,
                }
            })
        except Exception as identifier:
            print(traceback.format_exc())
            print(identifier)

    @http.route('/simontir/count_final/<int:id>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    def count_final(self, id, company_id):
        try:
            data = request.env['sale.order'].sudo().search_count([
                ('checker_id', '=', id),
                ('company_id', '=', int(company_id))
            ])

            return valid_response(status=200, data={
                'count': data,
            })
        except Exception as identifier:
            print(str(identifier))

    @http.route('/simontir/get_task/<path:no_ref>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def get_task(self, no_ref, company_id):
        try:

            no_ref = str(no_ref)

            sale = request.env['sale.order'].sudo().search_read([
                ('name', '=', no_ref),
                ('company_id', '=', int(company_id))
            ], fields=['x_nopol', 'x_waktu_mulai', 'x_is_wash'])

            so = request.env['account.analytic.account'].sudo().search_read([
                ('name', 'like', no_ref),
            ], fields=['project_ids'])

            tasks = request.env['project.task'].sudo().search_read([
                ('project_id', '=', so[0]['project_ids'][0]),
            ], fields=['name', 'x_status', 'x_state', 'x_duration'])

            saran = request.env['temporary.analisa'].sudo().search_read([
                ('x_ref_so', '=', sale[0]['id']),
            ])

            return valid_response(status=200, data={
                'count': len(tasks),
                'results': {
                    'waktu_mulai': sale[0]['x_waktu_mulai'],
                    'nopol': sale[0]['x_nopol'],
                    'cuci': sale[0]['x_is_wash'],
                    'id_saran': saran[0]['id'],
                    'saran': saran[0]['x_saran'],
                    'tasks': tasks
                }
            })
        except Exception as identifier:
            print(str(identifier))

    @http.route('/simontir/accept', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def accept(self, company_id = False):
        try:
            rq = request.jsonrequest
            task = request.env['project.task'].sudo().search([
                ('id', '=', rq['id']),
            ])

            task.write({
                "x_status": "accept"
            })

            hr = request.env['hr.employee'].sudo().search([
                ('user_id', '=', task[0]['user_id'][0]['id']),
            ])

            cek = request.env['account.analytic.line'].sudo().search([
                ('name', '=', task[0].name.split(':')[1]),
                ('task_id', '=', rq['id']),
            ])

            if len(cek) == 0:
                request.env['account.analytic.line'].sudo().create({
                    "name": task[0].name.split(':')[1],
                    "unit_amount": 1,
                    "user_id": task[0]['user_id'][0]['id'],
                    "partner_id": task[0]['user_id'][0]['id'],
                    "task_id": rq['id'],
                    "employee_id": hr[0].id if len(hr) > 0 else '',
                    "account_id": task.project_id[0].analytic_account_id[0].id,
                    "project_id": task.project_id.id,
                    "product_uom_id": task.project_id.sale_line_id.product_uom.id

                })

        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/reject', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def reject(self, company_id):
        try:
            rq = request.jsonrequest
            task = request.env['project.task'].sudo().search([
                ('id', '=', rq['id']),
                ('company_id', '=', int(company_id))
            ])

            task.write({
                "x_status": "reject"
            })

            hr = request.env['hr.employee'].sudo().search([
                ('user_id', '=', rq['user_id']),
                ('company_id', '=', int(company_id))
            ])

            cek = request.env['account.analytic.line'].sudo().search([
                ('name', '=', task[0].name.split(':')[1]),
                ('task_id', '=', rq['id']),
                ('company_id', '=', int(company_id))
            ])

            if len(cek) > 0:
                for c in cek:
                    c.unlink()

        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/finish_final', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def finish_final(self, invoice=None, company_id=None):
        try:
            rq = request.jsonrequest
            invoiced = invoice if invoice != None else rq['invoice']

            data = request.env['sale.order'].sudo().search([
                ('name', '=', invoiced),
            ])

            so = request.env['account.analytic.account'].sudo().search_read([
                ('name', 'like', invoiced),
            ], fields=['project_ids'])

            tasks = request.env['project.task'].sudo().search(
                [('project_id', '=', so[0]['project_ids'][0])])

            vehicle = request.env['fleet.vehicle'].sudo().search([
                ('license_plate', '=', data[0].x_nopol),
            ])[0].id

            service_type = request.env['fleet.service.type'].sudo().search([
                ('name', '=', 'Service Log'),
            ])

            if len(service_type) == 0:
                service_type = request.env['fleet.service.type'].sudo().create({
                    'name': 'Service Log',
                    'category': 'service'
                })

            payload = {
                'vehicle_id': vehicle,
                'odometer': request.env['fleet.vehicle.odometer'].sudo().search([('vehicle_id', '=', vehicle)], order="id desc")[0].value,
                'amount': data[0].amount_total,
                'date': data[0].confirmation_date,
                'purchaser_id': data[0].partner_id[0].id,
                'cost_subtype_id': service_type[0].id,
                'inv_ref': data[0].name,
                'x_mekanik': data[0].mekanik_id[0].id,
                'x_front_desk': data[0].write_uid[0].id
            }

            log = request.env['fleet.vehicle.log.services'].sudo().create(
                payload)
            cost_ids = request.env['fleet.vehicle.cost'].sudo().search([
                ('cost_subtype_id', '=', log[0].cost_subtype_id[0].id), 
                ('vehicle_id', '=', vehicle),
            ], order="id desc")

            for task in tasks:
                name_history = task.name.split(':')[1]
                if task.sale_line_id:
                    request.env['fleet.vehicle.cost'].sudo().create({
                        'description': task.sale_line_id.name,
                        'amount': task.sale_line_id.price_total,
                        'parent_id': cost_ids[0].id,
                        'vehicle_id': vehicle,
                    })
                else:
                    request.env['fleet.vehicle.cost'].sudo().create({
                        'description': name_history,
                        'amount': 0,
                        'parent_id': cost_ids[0].id,
                        'vehicle_id': vehicle,
                    })

            if 'user_cuci' in rq:
                if rq['user_cuci'] != "":
                    task_cuci = request.env['project.task'].sudo().search([
                        ('project_id', '=', so[0]['project_ids'][0]), 
                        ('description', 'like', '%CUCI MOTOR GRATIS'),
                    ])

                    task_cuci.write({
                        'user_id': rq['user_cuci']
                    })

            if len(data) > 0:
                data.write({
                    'invoice_status': 'to invoice'
                })

            return valid_response(status=200, data={
                'data': 'data'
            })

        except Exception as identifier:
            print(identifier)
            print(traceback.format_exc())

    @http.route('/simontir/lock_so', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def lock_so(self, company_id = False):
        try:
            rq = request.jsonrequest
            data = request.env['sale.order'].sudo().search([
                ('name', '=', rq['invoice']),
            ])

            request.env['temporary.analisa'].sudo().search([
                ('id', '=', rq['id_saran']),
            ]).write({
                'x_saran': rq['saran']
            })

            if len(data) > 0:
                data.action_done()

                data.write({
                    'x_is_reject': False,
                    'invoice_status': 'no',
                    'x_duration': rq['duration'],
                })

                if data[0]['x_antrian_service'] == 'Light Repair':
                    self.finish_final(rq['invoice'])

            return valid_response(status=200, data={
                'data': data
            })

        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/unlock_so', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def unlock_so(self, company_id):
        try:
            rq = request.jsonrequest
            data = request.env['sale.order'].sudo().search([
                ('name', '=', rq['invoice']),
                ('company_id', '=', int(company_id))
            ])

            if len(data) > 0:
                data.action_unlock()

                data.write({
                    'x_is_reject': True
                })

            return valid_response(status=200, data={
                'data': data
            })

        except Exception as identifier:
            print(identifier)

    def get_attendance(self, id):
        day = date.today().day
        month = date.today().month
        year = date.today().year

        employee = request.env['hr.employee'].sudo().search([
            ('user_id', '=', id),
        ])

        attendance = request.env['hr.attendance'].sudo().search([
            ('employee_id', '=', employee[0]['id']), 
            ('check_in', '>=', str((datetime.now()).date())), 
            ('check_in', '<', str((datetime.now() + timedelta(days=1)).date()))
        ])

        return attendance

    @http.route('/simontir/task/finish', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def finishTask(self, company_id = False):
        try:
            rq = request.jsonrequest
            data = request.env['project.task'].sudo().search([
                ('id', '=', rq['id']),
            ])

            task = data[0]['name'].split('sparepart')
            attendance = self.get_attendance(rq['user_id'])[0]

            if len(task[0].split('keluhan')) == 1:

                if len(task) == 2:
                    name = task[1].split(':')[1]
                else:
                    name = task[0].split(':')[1]

                product = request.env['product.template'].sudo().search([
                    ('name', '=', name),
                ])

                if len(task) == 2:
                    attendance.write({
                        'intensif_part': attendance.intensif_part + product[0]['x_ins_part'],
                        'total_part': attendance.total_part + 1,
                        'intensif_counter': attendance.intensif_counter + 1,
                    })
                else:
                    if task == 'CUCI MOTOR GRATIS':
                        attendance.write({
                            'ins_cuci_motor': attendance.ins_cuci_motor + 1000,
                        })
                    else:
                        attendance.write({
                            'intensif_jasa': attendance.intensif_jasa + product[0]['x_ins_jasa'],
                            'total_jasa': attendance.total_jasa + 1,
                            'intensif_counter': attendance.intensif_counter + 1,
                        })

            if len(data) > 0:
                data.write({
                    'x_state': 'finished',
                    'x_duration': rq['x_duration'],
                })

            return valid_response(status=200, data={
                'data': data[0].x_state
            })

        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/task/unfinish', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def unfinishTask(self, company_id = False):
        try:
            rq = request.jsonrequest
            data = request.env['project.task'].sudo().search([
                ('id', '=', rq['id']),
            ])

            task = data[0]['name'].split('sparepart')
            attendance = self.get_attendance(rq['user_id'])[0]

            if task[0].split('keluhan') == 1:

                if len(task) == 2:
                    name = task[1].split(':')[1]
                else:
                    name = task[0].split(':')[1]

                product = request.env['product.template'].sudo().search([
                    ('name', '=', name),
                ])

                if len(task) == 2:
                    attendance.write({
                        'intensif_part': attendance.intensif_part - product[0]['x_ins_part'],
                        'total_part': attendance.total_part - 1,
                        'intensif_counter': attendance.intensif_counter - 1,
                        'total_ue': attendance.total_ue - 1,
                    })
                else:
                    if task == 'CUCI MOTOR GRATIS':
                        attendance.write({
                            'ins_cuci_motor': attendance.ins_cuci_motor - 1000,
                        })
                    else:
                        attendance.write({
                            'intensif_jasa': attendance.intensif_jasa - product[0]['x_ins_jasa'],
                            'total_jasa': attendance.total_jasa - 1,
                            'intensif_counter': attendance.intensif_counter - 1,
                            'total_ue': attendance.total_ue - 1,
                        })

            if len(data) > 0:
                data.write({
                    'x_state': 'unfinished'
                })

            return valid_response(status=200, data={
                'data': data
            })

        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/get_cuci/<user_id>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def get_cuci(self, user_id, company_id):
        try:
            res = request.env['project.task'].sudo().search([
                ('name', 'like', '%CUCI MOTOR GRATIS'),
                ('timesheet_ids', '=', False),
                ('user_id', '=', int(user_id)),
                ('company_id', '=', int(company_id))
            ])

            data = [{
                "projectId": d.project_id.id,
                "projectName": d.project_id.name,
                "namaSo": d.sale_line_id.order_id.name,
                "nopol": d.sale_line_id.order_id.x_nopol,
                "typeMotor": d.sale_line_id.order_id.x_type_motor,
                "namaPemilik": d.sale_line_id.order_id.partner_id.name,
                "taskId": d.id,
                "taskName": d.name,
            }for d in res]

            return valid_response(status=200, data={
                'data': data
            })
        except Exception as e:
            print(str(e))

    @http.route('/simontir/cekNoMesin', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def cekNoMesin(self, company_id, *args, **kwargs):
        try:
            req = request.jsonrequest

            if len(req) > 1:
                cek = request.env['fleet.vehicle'].sudo().search([
                    ('vin_sn', '=', req['nomesin']),
                ])

                if len(cek) > 0:
                    if cek[0].license_plate != req['nopol']:
                        return False

            return True
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
