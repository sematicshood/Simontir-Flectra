# -*- coding: utf-8 -*-

{
    'name': 'Payment Acquirer',
    'author': 'Odoo S.A',
    'category': 'Accounting',
    'summary': 'Payment Acquirer Base Module',
    'version': '1.0',
    'description': """Payment Acquirer Base Module""",
    'depends': ['account'],
    'data': [
        'data/account_data.xml',
        'data/payment_icon_data.xml',
        'data/payment_acquirer_data.xml',
        'views/payment_views.xml',
        'views/account_payment_views.xml',
        'views/payment_templates.xml',
        'views/payment_portal_templates.xml',
        'views/assets.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',
        'security/payment_security.xml',
    ],
    'installable': True,
    'auto_install': True,
}
