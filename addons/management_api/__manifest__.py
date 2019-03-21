# -*- coding: utf-8 -*-
{
    'name': "management_api",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/flectra/flectra/blob/master/flectra/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'fleet', 'product', 'project', 'base_automation', 'account', 'crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/fleet_models_product.xml',
        'views/vehicle_colors.xml',
        'views/action_on_create_customer.xml',
        'views/custom_field_product.xml',
        'views/wa_sender_form.xml',
        'views/setting_account_wablaster.xml',
        'views/trigger_wa_sender.xml',
    ],
}