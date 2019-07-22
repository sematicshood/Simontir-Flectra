# -*- coding: utf-8 -*-
{
    'name': "sem_custom_field_sales_order",

    'summary': """
        Addon modul bengkel""",

    'description': """
        this addon will handle detail vehicle
    """,

    'author': "Sematics.id",
    'website': "http://sematics.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'development',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/salecustomfield.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}