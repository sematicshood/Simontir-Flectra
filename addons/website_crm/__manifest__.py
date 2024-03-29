{
    'name': 'Contact Form',
    'category': 'Website',
    'sequence': 54,
    'website': 'https://flectrahq.com/page/website-builder',
    'summary': 'Create Leads From Contact Form',
    'version': '2.0',
    'description': "",
    'depends': ['website_form', 'website_partner', 'crm'],
    'data': [
        'data/website_crm_data.xml',
        'views/crm_lead_view.xml',
        'views/website_crm_templates.xml',
        'views/res_config_settings_views.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'auto_install': True,
}
