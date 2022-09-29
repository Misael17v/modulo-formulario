# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BookCategory(models.Model):
    _name='libreria.libro.categoria'
    _parent_store=True
    _parent_name="parent_id"
    
    name=fields.Char('Categoria')
    description=fields.Text('Descripcion')
    
    parent_id=fields.Many2one(
        'libreria.libro.categoria',
        string='Categorias Principal',
        ondelete='restrict',
        index=True
    )
    
    child_ids = fields.One2many(
        'libreria.libro.categoria', 'parent_id',
        string='Categorias Secundario')
    parent_path = fields.Char(index=True)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')
    
   
    