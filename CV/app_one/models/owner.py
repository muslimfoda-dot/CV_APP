from odoo import models,fields



class Owner(models.Model):
    _name = "owner"

    name = fields.Char(string="Name")
    phone = fields.Char(string="number phone",size =11)
    address = fields.Char(string="address")
    name_ids = fields.One2many('app_one','owner',string="Tag name")

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'This name is not unique!')
    ]