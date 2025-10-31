from odoo import api, fields, models, _
from datetime import date



class Renewed(models.Model):
    _name = 'renewed.information'
    _description = 'Renewed'
    _rec_name = 'contract_number'

    contract_number = fields.Many2one('contract.information', ondelete='cascade')

    expiry_date = fields.Date(string="Expiry Date")
    renewed_date = fields.Date(string="Renewed Date")

    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    renewed_amount = fields.Monetary(
        string="Contract Amount",
        currency_field='currency_id'
    )

    state_renewed = fields.Selection(
        [('renewed', 'Renewed')], 
            default='renewed', string="Status", group_expand='_expand_groups')
    