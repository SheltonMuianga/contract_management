# -*- coding: utf-8 -*-
# Copyright 2022-Today shelton.
from odoo import api, fields, models, _
from datetime import date



class Contract(models.Model):
    """Contract Information"""
    _name = 'contract.information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = __doc__
    _rec_name = 'contract_number'

    contract_number = fields.Char(
        string='Contract Number',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )

    renewed_ids = fields.One2many('renewed.information', 'contract_number', string="Renewed Information")

    history_of_payments_ids = fields.One2many('history_of_payments.information', 'contract_number', string="History Of Payments")

    provider_ids = fields.Many2one('provider.information', string="Provider")

    provider_rate = fields.Many2one('rate.information', string="Provider Rate")

    @api.onchange('provider_ids')
    def _onchange_provider_id(self):
        if self.provider_ids:
            self.provider_rate = self.provider_ids.rate_ids.id
        else:
            self.provider_rate = False    

    contract_type_ids = fields.Many2one('contract_type.information', string="Contract Type")

    departments_ids = fields.Many2one('departments.information', string="Department")
    
    issue_date = fields.Date(string="Issue Date", default=fields.Date.context_today)
    expiry_date = fields.Date(string="Expiry Date")
    renewed_box = fields.Boolean(string="Renewed?")

    payment_method = fields.Selection(string="Payment Method",
        selection=[('one_time_payment', 'One Time Payment'), ('partial_payment', 'Partial Payment'), ('monthly_payment', 'Monthly Payment')])

    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    total_amount = fields.Monetary(
        string="Contract Amount",
        currency_field='currency_id'
    )

    monthly_amount = fields.Monetary(
        string="Monthly Amount",
        currency_field='currency_id'
    )

    cumulative_till_date = fields.Monetary(
        string="Cumulative Till Date",
        currency_field='currency_id'
    )

    balance_contract_value = fields.Monetary(
        string="Balance Contract Value",
        currency_field='currency_id'
    )

    observations = fields.Text(string="Observations")
    
    attachment_ids = fields.One2many('contract.attachment', 'contract_id', string="Attachments")

    closed_reason = fields.Text(string="Closed Reason")

    closed_box = fields.Boolean(string="Close Contract")
    
    state = fields.Selection(
        [('running', "Running"), ('to_expire', "To Expire"), ('expired', "Expired"), ('closed', "Closed")], 
            default='running', string="Status", group_expand='_expand_groups')
    
    @api.depends('expiry_date')
    def _compute_state_based_on_expiry(self):
        """
        Automatically update state based on expiry_date:
        - running: > 30 days remaining
        - to_expire: <= 30 days remaining
        - expired: past expiry date
        - closed: manual, never changed automatically
        """
        today = date.today()
        for record in self:
            # If manually closed, skip automatic update
            if record.closed_box:
                record.state = 'closed'
                continue

            if record.renewed_box:
                record.state = 'running'
                continue

            if not record.expiry_date:
                record.state = 'running'
                continue

            days_left = (record.expiry_date - today).days
            if days_left < 0:
                record.state = 'expired'
            elif days_left <= 30:
                record.state = 'to_expire'
            else:
                record.state = 'running'

    @api.onchange('expiry_date', 'closed_box','renewed_box')
    def _onchange_dates_and_close(self):
        """Update state automatically when expiry_date, closed_box, renewed_box changes."""
        self._compute_state_based_on_expiry()

    @api.model
    def _cron_update_expiry_states(self):
        """Cron job to update states daily (excluding manually closed records)."""
        records = self.search([])
        for record in records:
            record._compute_state_based_on_expiry()

    @api.model
    def _expand_groups(self):
        return ['running', 'to_expire', 'expired', 'closed']

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Get issue_date, default today
            issue_date_str = vals.get('issue_date', fields.Date.context_today(self))
            
            # Convert string to date object if needed
            if isinstance(issue_date_str, str):
                issue_date = fields.Date.from_string(issue_date_str)
            else:
                issue_date = issue_date_str

            # Format date as string for contract_number
            date_str = issue_date.strftime('%Y-%m-%d')

            # Count existing contracts for this date
            last_number = self.search_count([('issue_date', '=', issue_date)])
            sequence_number = str(last_number + 1).zfill(6)

            # Generate contract number
            vals['contract_number'] = f"CONTRACT/{date_str}/{sequence_number}"

        return super(Contract, self).create(vals_list)

    def write(self, vals):
        res = super(Contract, self).write(vals)
        return res
    
class ContractAttachment(models.Model):
    _name = 'contract.attachment'
    _description = 'Contract Attachments'

    name = fields.Char(string="File Name")
    file = fields.Binary(string="File", attachment=True)
    contract_id = fields.Many2one('contract.information', string="Contract")