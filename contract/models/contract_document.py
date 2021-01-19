# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ContractDocument(models.Model):
    _name = "documents.document"
    _inherit = "documents.document"

    contract_id = fields.Many2one('contract.contract', string="Contract")