from odoo import models,fields


class AppOneHistory(models.Model):
    _name = 'history'
    _description = 'app one history'


    user_id = fields.Many2one('res.users')
    app_one = fields.Many2one('app_one')
    old_state = fields.Char()
    new_state = fields.Char()
    reason = fields.Char()
    line_ids =fields.One2many('app_one_history_line','app_one_id')







class AppOneHistoryLine(models.Model):
    _name = 'app_one_history_line'

    description = fields.Text(string="Description")
    app_one_id = fields.Many2one('history')
    code = fields.Char(string="CODE")



