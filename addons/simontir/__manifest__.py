# -*- coding: utf-8 -*-
{
    'name': "simontir",

    'summary': """
        Modul khusus menangani Bengkel Motor dan mobil versi indonesia""",

    'description': """
        Manajemen data bengkel motor dan mobil
    """,

    'author': "sematics",
    'website': "http://sematics.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Vertical',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/lapHarian.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}