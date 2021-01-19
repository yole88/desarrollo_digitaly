# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Contract product',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Contract product',
    'description': """
          Contract product
""",
    'website': 'https://www.odoo.com',
    'depends': ['product', 'contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/menu_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
