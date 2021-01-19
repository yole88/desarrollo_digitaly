# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ContractProductState(models.Model):
    _name = 'contract_product.state'
    _description = 'Contract product state'

    name = fields.Char('Name', required=True)


class AttributesProductWarehouse(models.Model):
    _name = 'contract_product.warehouse'
    _description = 'Attributes product warehouse'

    name = fields.Char('Name', required=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    type = fields.Selection(selection_add=[
        ('warehouse', 'Warehouse')
    ], tracking=True, ondelete={'warehouse': 'set default'})

    state_id = fields.Many2one('contract_product.state', string='Product state')
    available = fields.Boolean('Available', default=True)
    attributes_ids = fields.One2many('contract_product.line', 'product_id', 'Attributes')
    image_ids = fields.One2many('contract_product.image', 'product_id', 'Images')


class ProductWarehouseLine(models.Model):
    _name = 'contract_product.line'
    _description = 'Product warehouse line'

    attributes_id = fields.Many2one('contract_product.warehouse', string='Attribute')
    product_id = fields.Many2one('product.template', string='Product')


class ProductImage(models.Model):
    _name = 'contract_product.image'
    _description = 'Product image'

    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    image_128 = fields.Binary('Image', related="image_1920")
    color = fields.Integer('Color Index', default=1)
    title = fields.Char('Title')
    product_id = fields.Many2one('product.template', string='Product')






