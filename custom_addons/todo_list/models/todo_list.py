from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TodoList(models.Model):
    _name = 'todo.list'
    _description = 'Todo List'

    name = fields.Char('Title', required= True)
    tag_ids = fields.Many2many('todo.list.tag',string='Tags')
    start_date = fields.Datetime('Start Date', required=True)
    end_date = fields.Datetime('End Date', required = True)

    state = fields.Selection([
        ('draft','DRAFT'),
        ('in_progress','IN_PROGRESS'),
        ('complete','COMPLETE')
    ], default='draft')

    item_ids = fields.One2many('todo.list.item', 'todo_id',string='List')
    attendee_ids = fields.Many2many('res.users', string='Attendees')
    all_done = fields.Boolean(compute='_compute_all_done')

    @api.constrains('start_date','end_date')
    def _check_date(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.end_date <= rec.start_date:
                raise ValidationError("End Date ต้องมากกว่า Start Date")
    @api.depends('item_ids.is_done')
    def _compute_all_done(self):
        for rec in self:
            rec.all_done= all(i.is_done for i in rec.item_ids) if rec.item_ids else False
    def action_progress(self):
        self.state = 'in_progress'
    def action_done(self):
        self.state = 'complete'

class TodoListItem(models.Model):
    _name = 'todo.list.item'
    _description = 'Todo Item' 
    todo_id = fields.Many2one('todo.list',ondelete='cascade')
    name = fields.Char('Name', required=True)
    description = fields.Char('Description')
    is_done = fields.Boolean('Is Complete')

class TodoListTag(models.Model):
    _name = 'todo.list.tag'
    _description = 'Tool Tag'
    name = fields.Char('Tag Name',required = True)      