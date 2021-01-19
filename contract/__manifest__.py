# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Contract',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Contract',
    'description': """
          Contract for sale
""",
    'website': 'https://www.odoo.com',
    'depends': ['base', 'sale_management', 'documents'],
    'data': [
        'security/contract_security.xml',
        'security/ir.model.access.csv',
        'data/data_state.xml',
        'views/contract_view.xml',
        'views/document_view.xml',
        'views/sale_view.xml',
        'views/partner_view.xml',
        'views/menu_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
