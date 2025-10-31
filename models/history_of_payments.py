from odoo import api, fields, models, _




class HistoryOfPayments(models.Model):
    _name = 'history_of_payments.information'
    _description = 'History Of Payments'

    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    contract_number = fields.Many2one('contract.information', ondelete='cascade')

    payment_method = fields.Selection(related='contract_number.payment_method', store=False)


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

    state_money = fields.Selection(
        [('paid', 'Paid'), ('unpaid', 'Unpaid')], 
            string="Payment Status",default='unpaid', group_expand='_expand_groups')
    
    def action_mark_paid(self):
        for rec in self:
            rec.state_money = 'paid'

    def action_mark_unpaid(self):
        for rec in self:
            rec.state_money = 'unpaid'