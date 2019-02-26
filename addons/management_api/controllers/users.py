from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback

class UsersAPIBentar(http.Controller):
    @http.route('/simontir/users/getAsistenMekanik', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getAsistenMekanik(self):
        hr    = request.env['hr.job'].sudo().search_read([('name','ilike','Asisten Mekanik')])[0]['employee_ids']

        hrs   = request.env['hr.employee'].sudo().search_read([('id','in',hr)])

        usrs  = [h['user_id'][0] if h['user_id'] is not False else None for h in hrs]
        usrs.remove(None)


        users = request.env['res.users'].search_read([
            ('id','in',usrs)
        ], fields=['name', 'role'])

        return valid_response(status=200, data={
                'count': len(users),
                'results': users
            })

    @http.route('/simontir/users/getUsersCuci', type="http", auth="none", method=['GET', 'OPTIONS'], csrf=False, cors="*")
    def getUsersCuci(self):
        users = request.env['res.users'].sudo().search_read([('role','=','Cuci')], fields=['name'])

        return valid_response(status=200, data={
                'count': len(users),
                'results': users
            })

    # TODO
    # Tambahin filter tanggal range bulan ini
    @http.route('/simontir/users/getTotalService/<user>', type="http", auth="none", method=['GET', 'OPTIONS'], csrf=False, cors="*")
    def getTotalService(self, user):
        users = request.env['sale.order'].sudo().search_count([('mekanik_id','=',int(user)), ('state','=','done')])

        return valid_response(status=200, data={
                'results': users
            })

    @http.route('/simontir/users/updateRoleUser', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")        
    # @authentication
    def updateRoleUser(self, *args, **kwargs):
        try:
            req = request.jsonrequest

            if len(req) > 1:
                request.env['res.users'].sudo().search([('id','=',req['ids'])])[0].write({
                    'role': req['role']
                })

            return True
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())