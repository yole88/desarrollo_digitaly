# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class ResPartner(models.Model):
    _inherit = "res.partner"

    contract_count = fields.Integer(compute='_compute_contract_count', string='Contract')

    def _compute_contract_count(self):
        for partner in self:
            partner.contract_count = self.env['contract.contract'].search_count([
                                             ('partner_id', '=', partner.id),
                                             ('state_id.close_contract', '=', False)])

