from odoo import models,fields

class ChangeState(models.TransientModel):
    _name = 'change_state'

    cv_app = fields.Many2one('app_one')
    state = fields.Selection([('draft', 'Draft'),('pending', 'Pending')],default='draft')
    reason = fields.Char()

    def action_confirm(self):
        if self.cv_app.state == 'closed':
           self.cv_app.state = self.state
           self.cv_app.create_history_record('closed',self.state , self.reason)

