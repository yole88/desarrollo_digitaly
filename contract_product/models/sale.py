# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('order_line')
    def _constrains_product_available(self):
        for line in self.order_line:
            if line.product_id.type == 'warehouse' and not line.product_id.available:
                raise UserError(_("This product is not available for sale."))

    @api.model
    def create(self, values):
        sale = super(SaleOrder, self).create(values)
        if sale.contract_id or self._context.get('default_contract_id'):
            for line in sale.order_line:
                if line.product_id.type == 'warehouse' and line.product_id.available:
                    product_line = self.env['product.product'].search([
                                           ('id', '=', line.product_id.id)])
                    product_line.write({'available': False})
        return sale

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if 'contract_id' in vals:
            for sale in self:
                for line in sale.order_line:
                    if line.product_id.type == 'warehouse' and line.product_id.available:
                        product_line = self.env['product.product'].search([
                                               ('id', '=', line.product_id.id)])
                        product_line.write({'available': False})
        return res





