# -*- coding: utf-8 -*-
from flectra import http

# class Simontir(http.Controller):
#     @http.route('/simontir/simontir/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/simontir/simontir/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('simontir.listing', {
#             'root': '/simontir/simontir',
#             'objects': http.request.env['simontir.simontir'].search([]),
#         })

#     @http.route('/simontir/simontir/objects/<model("simontir.simontir"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('simontir.object', {
#             'object': obj
#         })