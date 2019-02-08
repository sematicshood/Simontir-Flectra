from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime

class BoardsAPIBentar(http.Controller):
    @http.route('/simontir/getso', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getso(self):
        try:
            so = request.env['sale.order'].sudo().search([
                ('invoice_status','!=','invoiced'),
                ('state','!=','cancel'),
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
            print('-'*100)

    @http.route('/simontir/getso_mekanik', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getso_mekanik(self):
        try:
            so = request.env['sale.order'].sudo().search([
                ('state','=','sent')
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
            
            return valid_response(status=200, data={
                    'count': len(data),
                    'results': data
                })
        except Exception as identifier:
            print(identifier)
            print('-'*100)

    @http.route('/simontir/getso_finalcheck', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getso_finalcheck(self):
        so = request.env['sale.order'].sudo().search([
            ('state','=','done'), ('invoice_status', '=', 'no')
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
        
        return valid_response(status=200, data={
                'count': len(data),
                'results': data
            })

    @http.route('/simontir/pick_so', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")        
    # @authentication
    def pick_so(self):
        try:
            rq    =  request.jsonrequest
            data  =  request.env['sale.order'].sudo().search([('name','=',rq['invoice'])])
            
            data.action_confirm()

            data.write({
                'invoice_status': 'no'
            })
            
            so    =  request.env['account.analytic.account'].sudo().search_read([('name','=',rq['invoice'])], fields=['project_ids'])

            request.env['sale.order'].sudo().search([('name','=',rq['invoice'])]).write({
                'x_waktu_mulai': datetime.datetime.now()
            })

            tasks =  request.env['project.task'].sudo().search([('project_id', '=', so[0]['project_ids'][0])])

            for order in data[0]['order_line']:
                if order.product_id[0].product_tmpl_id[0].type != 'service':
                    request.env['project.task'].sudo().create({
                        'name': rq['invoice'] + ' sparepart:' + 'Ganti ' + order.product_id[0].product_tmpl_id[0].name,
                        'user_id': rq['user_id'],
                        'company_id': tasks[0].company_id[0].id,
                        'email_from': tasks[0].email_from,
                        'priority': 'l',
                        'planned_hours': 1,
                        'project_id': so[0]['project_ids'][0]
                    })


            for task in tasks:
                task.write({
                    'user_id': rq['user_id']
                })

            keluhan = request.env['temporary.keluhan'].sudo().search([('x_ref_so','=',data[0]['id'])])

            for kel in keluhan:
                request.env['project.task'].sudo().create({
                    'name': rq['invoice'] + ' keluhan:' + kel.x_keluhan,
                    'user_id': rq['user_id'],
                    'company_id': tasks[0].company_id[0].id,
                    'email_from': tasks[0].email_from,
                    'priority': 'l',
                    'planned_hours': 1,
                    'task_seq': '',
                    'project_id': so[0]['project_ids'][0]
                })

        except Exception as identifier:
            print(identifier)
            
        pass

    @http.route('/simontir/get_final_detail/<no_ref>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def get_final_detail(self, no_ref):
        try:
            sale  =  request.env['sale.order'].sudo().search_read([('name','=',no_ref)], fields=['x_nopol', 'x_waktu_mulai', 'x_is_wash'])

            so    =  request.env['account.analytic.account'].sudo().search_read([('name','=',no_ref)], fields=['project_ids'])

            tasks =  request.env['project.task'].sudo().search_read([('project_id', '=', so[0]['project_ids'][0])], fields=['name', 'x_status'])

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
            print(identifier)

        pass

    @http.route('/simontir/get_task/<no_ref>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def get_task (self, no_ref):
        try:
            sale  =  request.env['sale.order'].sudo().search_read([('name','=',no_ref)], fields=['x_nopol', 'x_waktu_mulai', 'x_is_wash'])

            so    =  request.env['account.analytic.account'].sudo().search_read([('name','=',no_ref)], fields=['project_ids'])

            tasks =  request.env['project.task'].sudo().search_read([('project_id', '=', so[0]['project_ids'][0])], fields=['name', 'x_status'])

            saran   =   request.env['temporary.analisa'].sudo().search_read([('x_ref_so', '=', sale[0]['id'])])

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
            print(identifier)

        pass

    @http.route('/simontir/accept', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")        
    # @authentication
    def accept(self):
        try:
            rq    =  request.jsonrequest
            task  =  request.env['project.task'].sudo().search([('id','=',rq['id'])])

            task.write({
                "x_status": "accept"
            })

            hr    =  request.env['hr.employee'].sudo().search([('user_id','=',task[0]['user_id'])])

            cek   =  request.env['account.analytic.line'].sudo().search([
                ('name','=',task[0].name.split(':')[1]),
                ('task_id','=',rq['id'])
            ])

            if len(cek) == 0:
                request.env['account.analytic.line'].sudo().create({
                    "name": task[0].name.split(':')[1],
                    "unit_amount": 1,
                    "user_id": task[0]['user_id'],
                    "partner_id": task[0]['user_id'],
                    "task_id": rq['id'],
                    "employee_id": hr[0].id,
                    "account_id": task.project_id[0].analytic_account_id[0].id
                })

        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/reject', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")        
    # @authentication
    def reject(self):
        try:
            rq    =  request.jsonrequest
            task  =  request.env['project.task'].sudo().search([('id','=',rq['id'])])

            task.write({
                "x_status": "reject"
            })

            hr    =  request.env['hr.employee'].sudo().search([('user_id','=',rq['user_id'])])

            cek   =  request.env['account.analytic.line'].sudo().search([
                ('name','=',task[0].name.split(':')[1]),
                ('task_id','=',rq['id'])
            ])

            if len(cek) > 0:
                for c in cek:
                    c.unlink()

        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/finish_final', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")        
    # @authentication
    def finish_final(self):
        try:
            rq    =  request.jsonrequest
            data  =  request.env['sale.order'].sudo().search([('name','=',rq['invoice'])])

            so    =  request.env['account.analytic.account'].sudo().search_read([('name','=',rq['invoice'])], fields=['project_ids'])

            tasks =  request.env['project.task'].sudo().search([('project_id', '=', so[0]['project_ids'][0]), ('description', 'like', 'Cuci Motor')])

            tasks.write({
                'user_id': rq['user_cuci']
            })

            if len(data) > 0:
                data.write({
                    'invoice_status': 'to invoice'
                })

            return valid_response(status=200, data={
                'data': data
            })

        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/lock_so', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")        
    # @authentication
    def lock_so(self):
        try:
            rq    =  request.jsonrequest
            data  =  request.env['sale.order'].sudo().search([('name','=',rq['invoice'])])

            if len(data) > 0:
                data.action_done()

                data.write({
                    'x_is_reject': False,
                    'invoice_status': 'no'
                })

            return valid_response(status=200, data={
                'data': data
            })

        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/unlock_so', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")        
    # @authentication
    def unlock_so(self):
        try:
            rq    =  request.jsonrequest
            data  =  request.env['sale.order'].sudo().search([('name','=',rq['invoice'])])
            
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