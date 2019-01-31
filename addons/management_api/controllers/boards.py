from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime

class BoardsAPIBentar(http.Controller):
    @http.route('/simontir/getso', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    @authentication
    def getso(self):
        so = request.env['sale.order'].sudo().search([
            ('state','!=','done'),
            ('state','!=','cancel'),
        ], order="id asc")

        data = [{
            "no_polisi": s.x_nomer_polisi,
            "customer": s.partner_id[0].name,
            "tipe_kenadaraan": s.x_tipe_kendaraan,
            "status": s.state,
            "invoice": s.invoice_status,
            "antrian_service": s.x_antrian_service,
            "order_line": [{
                "name": o.name,
                "type": o.product_id[0].product_tmpl_id[0].type
            } for o in s.order_line]
        } for s in so]
        
        return valid_response(status=200, data={
                'count': len(data),
                'results': data
            })

    @http.route('/simontir/getso_mekanik', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    @authentication
    def getso_mekanik(self):
        so = request.env['sale.order'].sudo().search([
            ('state','=','sent'),
        ], order="id asc")
        print(so)

        data = [{
            "no_polisi": s.x_nomer_polisi,
            "customer": s.partner_id[0].name,
            "tipe_kenadaraan": s.x_tipe_kendaraan,
            "status": s.state,
            "invoice": s.invoice_status,
            "antrian_service": s.x_antrian_service,
            "name": s.name,
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
    @authentication
    def pick_so(self):
        try:
            rq    =  request.jsonrequest
            data  =  request.env['sale.order'].sudo().search([('name','=',rq['invoice'])]).action_confirm()
            
            so    =  request.env['account.analytic.account'].sudo().search_read([('name','=',rq['invoice'])], fields=['project_ids'])

            request.env['sale.order'].sudo().search([('name','=',rq['invoice'])]).write({
                'x_waktu_mulai': datetime.datetime.now()
            })

            tasks =  request.env['project.task'].sudo().search([('project_id', '=', so[0]['project_ids'][0])])

            for task in tasks:
                task.write({
                    'user_id': rq['user_id']
                })

            keluhan = request.env['temporary.keluhan'].sudo().search([('x_ref_so','=',rq['invoice'])])

            for kel in keluhan:
                request.env['project.task'].sudo().create({
                    'name': rq['invoice'] + ' keluhan:' + kel.x_keluhan,
                    'user_id': rq['user_id'],
                    'company_id': tasks[0].company_id[0].id,
                    'email_from': tasks[0].email_from,
                    'priority': 'l',
                    'planned_hours': 1,
                    'project_id': so[0]['project_ids'][0]
                })

        except Exception as identifier:
            print(identifier)
            
        pass

    @http.route('/simontir/get_task/<no_ref>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    @authentication
    def getso(self, no_ref):
        try:
            sale  =  request.env['sale.order'].sudo().search_read([('name','=',no_ref)], fields=['x_nomer_polisi', 'x_waktu_mulai'])

            so    =  request.env['account.analytic.account'].sudo().search_read([('name','=',no_ref)], fields=['project_ids'])

            tasks =  request.env['project.task'].sudo().search_read([('project_id', '=', so[0]['project_ids'][0])], fields=['name'])

            return valid_response(status=200, data={
                'count': len(tasks),
                'results': {
                    'waktu_mulai': sale[0]['x_waktu_mulai'],
                    'nopol': sale[0]['x_nomer_polisi'],
                    'tasks': tasks
                }
            })
        except Exception as identifier:
            print(identifier)

        pass

    @http.route('/simontir/lock_so', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")        
    @authentication
    def lock_so(self):
        try:
            rq    =  request.jsonrequest
            data  =  request.env['sale.order'].sudo().search([('name','=',rq['invoice'])]).action_done()

            return valid_response(status=200, data={
                'data': data
            })

        except Exception as identifier:
            print(identifier)

    @http.route('/simontir/unlock_so', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")        
    @authentication
    def unlock_so(self):
        try:
            rq    =  request.jsonrequest
            data  =  request.env['sale.order'].sudo().search([('name','=',rq['invoice'])]).action_unlock()

            return valid_response(status=200, data={
                'data': data
            })

        except Exception as identifier:
            print(identifier)