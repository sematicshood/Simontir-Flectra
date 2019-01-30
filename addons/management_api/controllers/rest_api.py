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
    @authentication
    def index(self, **get):
        data = request.jsonrequest

        uid  = request.session.authenticate(flectra.tools.config['db_name'], data['login'], data['password'])
        user = request.env['res.users'].search_read([
            ('id','=',uid)
        ], fields=['image', 'name', 'role'])

        if uid is not False:
            return valid_response(status=200, data=user)
        else:
            info = "Username or Password is incorrect!!"
            error = 'username_or_password_name_incorrect'
            _logger.error(info)
            return invalid_response(400, error, info)