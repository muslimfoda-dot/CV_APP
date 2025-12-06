from odoo import models,fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    cv_app = fields.Many2one('app_one')
    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()
        print("inside action confirm")
        return res
