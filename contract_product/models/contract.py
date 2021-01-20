# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Contract(models.Model):
    _inherit = 'contract.contract'

    def write(self, vals):
        res = super(Contract, self).write(vals)
        if 'state_id' in vals:
            for contract in self:
                if contract.state_id.close_contract:
                    for c in contract.sale_ids:
                        for line in c.order_line:
                            if line.product_id.type == 'warehouse':
                                product_line = self.env['product.product'].search([
                                                       ('id', '=', line.product_id.id)])
                                product_line.write({'available': True})
        return res





