# -*- coding: utf-8 -*-
from flectra import http

# class PrintDotmatrix(http.Controller):
#     @http.route('/print_dotmatrix/print_dotmatrix/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/print_dotmatrix/print_dotmatrix/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('print_dotmatrix.listing', {
#             'root': '/print_dotmatrix/print_dotmatrix',
#             'objects': http.request.env['print_dotmatrix.print_dotmatrix'].search([]),
#         })

#     @http.route('/print_dotmatrix/print_dotmatrix/objects/<model("print_dotmatrix.print_dotmatrix"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('print_dotmatrix.object', {
#             'object': obj
#         })