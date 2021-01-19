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




