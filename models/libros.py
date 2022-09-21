import string
from odoo import models, fields

class Libros(models.Model):
    _name = 'libros'
    
    name= fields.Char(string="Nombre del libro")
    editorial= fields.Char(string="Nombre de la editorial")
