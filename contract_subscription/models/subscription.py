# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Subscription(models.Model):
    _inherit = 'sale.subscription'

    contract_ids = fields.One2many('contract.contract', 'subscription_id', string='Contract ')
    subscription_count = fields.Integer(compute='_compute_subscription_count')

    def _compute_subscription_count(self):
        self.subscription_count = len(self.contract_ids)

    def write(self, vals):
        res = super(Subscription, self).write(vals)
        if 'stage_id' in vals:
            for subs in self:
                if subs.stage_id.category == 'closed' and subs.contract_ids:
                    self.close_contract()
                elif subs.stage_id.category != 'closed' and subs.contract_ids:
                    self.open_contract()
        return res

    def close_contract(self):
        res = []
        search = self.env['contract.state'].search
        for s in self:
            for contract in s.contract_ids:
                state = search([('close_contract', '=', True), ('sequence', '>=', contract.state_id.sequence)], limit=1)
                if not state:
                    state = search([('close_contract', '=', True)], limit=1)
                contract.write({'state_id': state.id, 'state': 'closed'})
        return res

    def open_contract(self):
        res = []
        search = self.env['contract.state'].search
        for s in self:
            for contract in s.contract_ids:
                state = search([('close_contract', '=', False), ('sequence', '>=', contract.state_id.sequence)], limit=1)
                if not state:
                    state = search([('close_contract', '=', False)], limit=1)
                contract.write({'state_id': state.id, 'state': 'draft'})
        return res

    def action_contract(self):
        self.ensure_one()
        contracts = self.env['contract.contract'].search([('subscription_id', 'in', self.ids)])
        return {
            'name': _('Contracts'),
            'res_model': 'contract.contract',
            'type': 'ir.actions.act_window',
            'views': [(False, 'tree')],
            'view_mode': 'tree',
            "domain": [["id", "in", contracts.ids]],
            'context': {
                "create": False
            }
        }


class Contract(models.Model):
    _inherit = 'contract.contract'

    subscription_id = fields.Many2one(
        'sale.subscription', string='Subscriptions', required=True)











