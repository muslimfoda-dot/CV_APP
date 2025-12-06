from odoo import models,fields,api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    app_one_id = fields.Many2one('app_one')
    # price = fields.Integer(related='app_one_id.number')
    price = fields.Integer(compute='_compute_price')


    @api.depends('app_one_id')
    def _compute_price(self):
        for ric in self:
            ric.price = ric.app_one_id.number