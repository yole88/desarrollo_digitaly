# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Contract subscription',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Contract product',
    'description': """
          Contract subscription
""",
    'website': 'https://www.odoo.com',
    'depends': ['sale_subscription', 'contract'],
    'data': [
        'views/subscription_view.xml',
        'views/contract_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
