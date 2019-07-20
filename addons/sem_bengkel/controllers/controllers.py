# -*- coding: utf-8 -*-
from flectra import http

# class SemBengkel(http.Controller):
#     @http.route('/sem_bengkel/sem_bengkel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sem_bengkel/sem_bengkel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sem_bengkel.listing', {
#             'root': '/sem_bengkel/sem_bengkel',
#             'objects': http.request.env['sem_bengkel.sem_bengkel'].search([]),
#         })

#     @http.route('/sem_bengkel/sem_bengkel/objects/<model("sem_bengkel.sem_bengkel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sem_bengkel.object', {
#             'object': obj
#         })