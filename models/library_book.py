# -*- coding: utf-8 -*-
from odoo import models, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char('Titulo', required=True)
    date_release = fields.Date('Fecha de creacion')
    active = fields.Boolean(default=True)
    author_ids = fields.Many2many('res.partner', string='Autores')
    state = fields.Selection(
        [('available', 'Disponible'),
         ('borrowed', 'Prestado'),
         ('lost', 'Perdido')],
        'estado', default="available")
    cost_price = fields.Float('Costo de libro')
    category_id = fields.Many2one('library.book.category')

    def make_available(self):
        self.ensure_one()
        self.state = 'available'

    def make_borrowed(self):
        self.ensure_one()
        self.state = 'borrowed'

    def make_lost(self):
        self.ensure_one()
        self.state = 'lost'


