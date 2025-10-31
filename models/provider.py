# -*- coding: utf-8 -*-
# Copyright 2022-Today shelton.
from odoo import api, fields, models, _
from datetime import datetime



class Provider(models.Model):
    """Provider Information"""
    _name = 'provider.information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = __doc__
    _rec_name = 'name'

    provider_id = fields.Char(
        string='Provider ID',
        copy=False,
        readonly=True,
    )
    name = fields.Char(string="Provider Name", required=True)
    rate_ids = fields.Many2one('rate.information', string="Provider Rate")

    comment_ids = fields.One2many('comments.information', 'provider_id', string="Comments")

class Comments(models.Model):
    _name = 'comments.information'
    _description = 'Comments'

    name = fields.Text(string="Comments")
    commented_by = fields.Many2one(
        'res.users', string='Commented by', default=lambda self: self.env.user, readonly=True)
    
    commented_date = fields.Datetime(string="Commented Date", default=lambda self: datetime.now(), readonly=True)

    provider_id = fields.Many2one('provider.information', string="Provider", ondelete='cascade')
