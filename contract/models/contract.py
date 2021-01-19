# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime, date
from odoo.exceptions import UserError


class ContractState(models.Model):
    _name = 'contract.state'
    _description = 'Contract state'

    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active', default=True)
    close_contract = fields.Boolean('Close contract')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 readonly=True, index=True, default=lambda self: self.env.company,
                                 )


class Contract(models.Model):
    _name = 'contract.contract'
    _description = 'Contract'

    name = fields.Char('Name', required=True,
                       help='Object of the contract')
    number = fields.Char('Number', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    date_start = fields.Date('Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date('End Date', required=True,)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 readonly=True, index=True, default=lambda self: self.env.company,
                                 help="Company contract")
    self_renewing = fields.Boolean('Self renewing')
    state_id = fields.Many2one('contract.state', string='Contract state', required=True)
    document_ids = fields.One2many('documents.document', 'contract_id', string="Documents")
    document_count = fields.Integer('Document Count', compute='_compute_document_count')
    sale_ids = fields.One2many('sale.order', 'contract_id', 'Sale Orders')
    sale_count = fields.Integer(string='Sale Orders', compute='_get_count_sale')
    user_id = fields.Many2one('res.users', string='Commercial', default=lambda self: self.env.uid)
    is_closed = fields.Boolean(related='state_id.close_contract')
    state = fields.Selection([('draft', 'New'),
                              ('closed', 'Closed')],
                             'Status',
                             track_visibility='onchange', default='draft')

    def _compute_document_count(self):
        read_group_var = self.env['documents.document'].read_group(
            [('contract_id', 'in', self.ids)],
            fields=['contract_id'],
            groupby=['contract_id'])

        document_count_dict = dict((d['contract_id'][0], d['contract_id_count']) for d in read_group_var)
        for record in self:
            record.document_count = document_count_dict.get(record.id, 0)

    def action_documents(self):
        self.ensure_one()
        value = {
            'name': _('Documents'),
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            'views': [(False, 'kanban')],
            'view_mode': 'kanban',
            'context': {
                "search_default_contract_id": self.id,
                "default_contract_id": self.id,
                "searchpanel_default_folder_id": False
            },
        }
        return value

    @api.onchange('date_start')
    def _set_end_date(self):
        if self.date_start:
            date_start = datetime.strftime(self.date_start, '%Y-%m-%d')
            start = datetime.strptime(date_start, "%Y-%m-%d")
            self.date_end = date(day=start.day, month=start.month, year=start.year + 1)

    @api.onchange('state_id')
    def _onchange_state(self):
        if self.state_id.close_contract:
            self.state = 'closed'
        else:
            self.state = 'draft'

    def _get_count_sale(self):
        self.sale_count = len(self.sale_ids)

    def unlink(self):
        for contract in self:
            if contract.state_id.close_contract:
                raise UserError(_('The contract cannot be deleted, its status is closed.'))
        return super(Contract, self).unlink()


class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_id = fields.Many2one('contract.contract', 'Contract')


