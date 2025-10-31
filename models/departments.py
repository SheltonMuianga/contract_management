# -*- coding: utf-8 -*-
# Copyright 2022-Today shelton.
from odoo import api, fields, models, _
from datetime import date



class Departments(models.Model):
    """Department Information"""
    _name = 'departments.information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = __doc__
    _rec_name = 'name'

    name = fields.Char(string="Department Name", required=True)