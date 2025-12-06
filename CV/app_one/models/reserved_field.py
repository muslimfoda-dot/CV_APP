from email.policy import default

from odoo import models,fields



class ReservedFiled(models.Model):
    _name = 'reserved_filed'
    _description = 'reserved record'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'description'

    no = fields.Integer()
    description = fields.Text()
    code = fields.Integer()
    active = fields.Boolean(default=True)
