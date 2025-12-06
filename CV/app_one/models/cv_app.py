from email.policy import default

from odoo import models, fields, api
from odoo.api import readonly
from odoo.exceptions import ValidationError
from odoo.fields import Many2one


class AppOne(models.Model):
    _name = 'app_one'
    _description = "app_one"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default="NEW REF", readonly=True)
    name = fields.Char(string="Name", required=True, default="NEW NAME", size=25)
    code = fields.Char(string="Code")
    player = fields.Char(string="Player")
    description = fields.Text(string="Description", tracking=True)
    table = fields.Boolean(string="table")
    number = fields.Integer(string="number", required=True)
    price = fields.Float(string="Price")
    selling_price = fields.Float(string="selling price ")
    diff = fields.Float(compute='_computed_diff', store=True)
    tag = fields.Many2many('tag')
    owner = fields.Many2one('owner')
    phone = fields.Char(related='owner.phone', readonly=False)
    address = fields.Char(related='owner.address', readonly=False)
    date_availability = fields.Datetime(tracking=True, default=fields.Datetime.now())
    expected_selling_date = fields.Date(tracking=True)
    is_late = fields.Boolean(tracking=True, readonly=True)
    state = fields.Selection([('draft', 'Draft'),   ('pending', 'Pending'), ('sold', 'SOLD'), ('closed', 'Closed'), ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'This name is not unique!')
    ]
    line_ids = fields.One2many('app_one_line', 'app_one_id')

    @api.constrains('number')
    def check_number_greater_zero(self):
        for rec in self:
            if rec.number == 0:
                raise ValidationError('please add number in number')

    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft')
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state = 'closed'

    @api.depends('price', 'selling_price')
    def _computed_diff(self):
        for rec in self:
            rec.diff = (rec.price or 0) - (rec.selling_price or 0)

    @api.onchange('selling_price')
    def _onchange_selling_price(self):
        for rec in self:
            if rec.selling_price and rec.selling_price < 0:
                return {
                    'warning': {
                        'title': 'Warning',
                        'message': 'This number is negative!',
                        'type': 'notification',
                    }
                }


    def check_expected_selling_date(self):
        app_one_ids = self.search([])
        for rec in app_one_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True


    def action(self):
        print(self.env['owner'].search([]))


    def create(self, vale):
        res = super(AppOne, self).create(vale)
        if res.ref == 'NEW REF':
            res.ref = self.env['ir.sequence'].next_by_code('app_one_seq')
        return res


    def create_history_record(self, old_state, new_state , reason=""):
        for rec in self:
            rec.env['history'].create({
                'user_id': rec.env.uid,
                'app_one': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
            })

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_action')
        action['context'] = {
            'default_cv_app': self.id,
        }
        return action
#         test this code v
    def action_write(self,default=None):
        res = super(AppOne,self).copy(default=default)

class AppOneLine(models.Model):
    _name = 'app_one_line'

    description = fields.Text(string="Description")
    app_one_id = fields.Many2one('app_one')
    code = fields.Char(string="CODE")
