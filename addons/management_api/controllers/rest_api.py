import functools
import hashlib
import os
import werkzeug.wrappers
import ast
try:
    import simplejson as json
except ImportError:
    import json
import flectra
from flectra import http
from flectra.http import request
from flectra import fields
from .rest_exception import *
from contextlib import closing

_logger = logging.getLogger(__name__)

def authentication(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        try:
            client_api    = request.httprequest.environ['HTTP_CLIENT_API']
            client_secret = request.httprequest.environ['HTTP_CLIENT_SECRET']
            
            #check authentication        
            cek = request.env['management_api.management_api'].sudo().search_count([
                ('client_api', '=', client_api),
                ('client_secret', '=', client_secret)
            ])

            if cek > 0:
                return func(self, *args, **kwargs)
            else:
                info = "Client api or client secret is incorrect!!"
                error = 'client_api_or_client_secret_incorrect'
                _logger.error(info)
                return invalid_response(400, error, info)

        except Exception as error:
            if str(error) == "'HTTP_CLIENT_API'":
                info = "Missing client api in request header!"
                error = 'client_api_not_found'
                _logger.error(info)
                return invalid_response(400, error, info)
                
            elif str(error) == "'HTTP_CLIENT_SECRET'":
                info = "Missing client secret in request header!"
                error = 'client_secret_not_found'
                _logger.error(info)
                return invalid_response(400, error, info)

    return wrap

class ControllerAPIBentar(http.Controller):
    @http.route('/simontir/login', type='json', auth="none", methods=['POST', 'OPTIONS'],
        csrf=False, cors="*")
    # @authentication
    def index(self, **get):
        data = request.jsonrequest

        try:
            request.session.authenticate(flectra.tools.config['db_name'], data['login'], data['password'])
        except:
            # Invalid database:
            info = "Invalid database!"
            error = 'invalid_database'
            _logger.error(info)
            return invalid_response(400, error, info)

        uid = request.session.uid
        # flectra login failed:
        if not uid:
            info = "flectra User authentication failed!"
            error = 'flectra_user_authentication_failed'
            _logger.error(info)
            return invalid_response(401, error, info)

        user = request.env['res.users'].sudo().search_read([
            ('id','=',uid)
        ], fields=['image', 'name', 'role', 'company_id', 'company_ids'])

        id_em = request.env['res.users'].sudo().search_read([
            ('id','=',uid)
        ])[0]['employee_ids'][0]

        company = request.env['res.company'].sudo().search_read([
            ('id', 'in', user[0]['company_ids'])
        ], fields=['name'])

        hr    = request.env['hr.employee'].sudo().search_read([('id','=',id_em)],
                    fields=['job_id']
                )

        user[0]['job']  =   hr[0]['job_id'][1]
        user[0]['companies'] = company

        # Successful response:
        if uid is not False:
            return valid_response(status=200, data=user).response
        else:
            info = "Username or Password is incorrect!!"
            error = 'username_or_password_name_incorrect'
            _logger.error(info)
            return invalid_response(400, error, info)

    @http.route('/simontir/getusers', type='http', auth="none", methods=['GET', 'OPTIONS'],
        csrf=False, cors="*")
    # @authentication
    def getusers(self, **get):
        try:
            data = request.env['res.users'].sudo().search_read([], fields=['name'])

            return valid_response(status=200, data={
                'count': len(data),
                'results': data
            })
        except Exception as identifier:
            print(identifier)