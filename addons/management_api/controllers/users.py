from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
from datetime import datetime, timedelta
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
    def getUsersCuci(self, company_id):
        users = request.env['res.users'].sudo().search_read([('role','=','Cuci')], fields=['name'])

        return valid_response(status=200, data={
                'count': len(users),
                'results': users
            })

    def getFirstDay(self, date):
        return datetime(date.year, date.month, 1).strftime('%Y-%m-%d')

    def getLastDay(self, date):
        year  = date.year
        month = date.month + 1

        if date.month == 12:
            year  = date.year + 1
            month = 1


        d   =   datetime(year, month, 1) - timedelta(days=1)
        
        return d.strftime('%Y-%m-%d')

    @http.route('/simontir/users/getTotalService/<user>', type="http", auth="none", method=['GET', 'OPTIONS'], csrf=False, cors="*")
    def getTotalService(self, user):
        try:
            domain = [
                ('mekanik_id','=',int(user)), 
                ('state','=','done'),
                ('create_date','>=',self.getFirstDay(datetime.today())),
                ('create_date','<=',self.getLastDay(datetime.today()))
            ]
            print(domain)

            users = request.env['sale.order'].sudo().search_count(domain)

            return valid_response(status=200, data={
                    'results': users
                })
        except Exception as identifier:
            pass

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