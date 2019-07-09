# -*- coding: utf-8 -*-
{
    'name': "Check Printing in Expenses",
    'author' : 'Odoo S.A',
    'summary': """Print amount in words on checks issued for expenses""",
    'category': 'Accounting',
    'description': """
        Print amount in words on checks issued for expenses
    """,
    'version': '1.0',
    'depends': ['account_check_printing', 'hr_expense'],
    'auto_install': True,
    'data': [
        'views/payment.xml',
    ],
}
