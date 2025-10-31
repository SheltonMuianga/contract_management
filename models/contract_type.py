# -*- coding: utf-8 -*-
# Copyright 2022-Today shelton.
from odoo import api, fields, models, _
from datetime import date



class Type(models.Model):
    """ContractType Information"""
    _name = 'contract_type.information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = __doc__
    _rec_name = 'name'

    name = fields.Char(string="Contract Type Name", required=True)
