from flectra import http
import flectra
from flectra.http import request
from . rest_api import authentication
from . rest_exception import *
import datetime
import traceback
from itertools import groupby


class ProfileAPI(http.Controller):
    @http.route('/simontir/job', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getJob(self, company_id=None):
        hr = request.env['hr.job'].sudo().search_read([], fields=['name'])

        return valid_response(status=200, data={
            'results': hr
        })


class ProfileAPI(http.Controller):
    @http.route('/simontir/job/create', type='json', auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def postJob(self):
        req = request.jsonrequest

        hr = request.env['assign.menu'].sudo().search([
            ('job_id', '=', req['job_id'])
        ])

        if len(hr) > 0:
            hr.write(req)
        else:
            request.env['assign.menu'].sudo().create(req)

        return valid_response(status=200, data={
            'results': 'success'
        })

class ProfileAPI(http.Controller):
    @http.route('/simontir/job/<int:job_id>/menus', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False, cors="*")
    # @authentication
    def getMenus(self, job_id, company_id):
        hr = request.env['assign.menu'].sudo().search_read([
            ('job_id', '=', int(job_id)),
        ], fields=['menus'])

        return valid_response(status=200, data={
            'results': hr
        })
