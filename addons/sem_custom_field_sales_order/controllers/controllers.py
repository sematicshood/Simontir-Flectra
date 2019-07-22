# -*- coding: utf-8 -*-
from flectra import http

# class SemCustomFieldSalesOrder(http.Controller):
#     @http.route('/sem_custom_field_sales_order/sem_custom_field_sales_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sem_custom_field_sales_order/sem_custom_field_sales_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sem_custom_field_sales_order.listing', {
#             'root': '/sem_custom_field_sales_order/sem_custom_field_sales_order',
#             'objects': http.request.env['sem_custom_field_sales_order.sem_custom_field_sales_order'].search([]),
#         })

#     @http.route('/sem_custom_field_sales_order/sem_custom_field_sales_order/objects/<model("sem_custom_field_sales_order.sem_custom_field_sales_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sem_custom_field_sales_order.object', {
#             'object': obj
#         })