
from odoo import models, fields,api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging

logger=logging.getLogger(__name__)

class LibraryBook(models.Model):
    _name='libreria.libro'
    _description='Libreria de Libro'
    
    name=fields.Char('Titulo',required=True)
    date_release=fields.Date('Fecha De Creacion')
    
    author_ids=fields.Many2many('res.partner',string='Autores')
    category_id=fields.Many2one('libreria.libro.categoria',string="Categoria")
    
    state=fields.Selection([
        ('draft','Indisponible'),
        ('available','Disponible'),
        ('borrowed','Prestado'),
        ('lost','Perdido')],
        'Estado', default='draft')
    
    @api.model
    def is_allowed_transition(self, old_state,new_state):
        allowed=[('draft','available'),
                 ('available','borrowed'),
                 ('borrowed','available'),
                 ('draft','borrowed'),
                 ('available','lost'),
                 ('borrowed','lost'),
                 ('lost','available'),
                 ('draft','lost'),
                 ('available','draft'),
                 ('lost','borrowed'),
                 ('borrowed','draft'),
                 ('lost','draft')]
        
        return(old_state,new_state) in allowed
    
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state,new_state):
                book.state=new_state
            else:
                msg=_('Moving from %s to %s is not allowed')%(book.state, new_state)
                raise UserError(msg)
    
    def make_draft(self):
        self.change_state('draft')
            
    def make_available(self):
        self.change_state('available')
        
    def make_borrowed(self):
        self.change_state('borrowed')
        
    def make_lost(self):
        self.change_state('lost')
        
#obtencion de un conjunto de registros vacio para un modelo diferente
    def log_all_library_members(self):
        library_member_model = self.env['libreria.miembros']  # This is an empty recordset of model library.member
        all_members = library_member_model.search([])
        print("ALL MEMBERS:", all_members)
        return True

#
     ##craenando nuevo modulo
    def create_categories(self):
        categ1={
            'name':'Categoria Secundario 1',
            'description':'Descripciion de la Categoria 1'
        }

        categ2={
            'name':'Categoria Secundaria 2',
            'description':'Descripcion de la categoria 2'
        }
        
        ##multiple_records = self.env['libreria.libro.categoria'].create([categ1,categ2])
        parent_category_val = {
            'name': 'name',
            'description': 'Esta funcionando parent_category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        
        record=self.env['libreria.libro.categoria'].create(parent_category_val)
        return True
    ##
    
    ###Actualizar valores de registros de conjuntos de registros
    def change_release_date(self):
        self.ensure_one()
        ###self.update({
          ###  'date_release':fields.Datetime.now(),
            ###'another_field':'value'
        ###})
        self.date_release=fields.Date.today()
    ###
    
    ####Busqueda de registros
    def find_book(self):
        domain = [
            '|',
                '&', ('name', 'ilike', 'Book Name'),
                     ('category_id.name', '=', 'Category Name'),
                     
                '&', ('name', 'ilike', 'Book Name 2'),
                     ('category_id.name', '=', 'Category Name 2')
        ]
        books = self.search(domain)
        logger.info('Books found: %s', books)
        return True
        
    ####def find_partner(self):
        ####PartnerObj=self.env['res.partner']
        ####domain=[
            ####'&', ('name', 'ilike', 'Book name'),
                #### ('category_id.name', '=', 'Odoo')
        ####]
        ####partner=PartnerObj.search(domain)
    ####
   #####filtrado de registros
    def filter_books(self):
        all_books = self.search([])
        filtered_books = self.books_with_multiple_authors(all_books)
        logger.info('Filtered Books: %s', filtered_books)

    @api.model
    def books_with_multiple_authors(self, all_books):
        def predicate(book):
            if len(book.author_ids) > 1:
                return True
        return all_books.filtered(predicate)
    
        
   #####
   
   ###### relaciones de conjunto de registros
    def mapped_books(self):
        all_books = self.search([])
        books_authors = self.get_author_names(all_books)
        logger.info('Books Authors: %s', books_authors)

    @api.model
    def get_author_names(self, all_books):
        return all_books.mapped('author_ids.name')
    
     ######   
     
     
     #######ordenar registros
    def sort_books(self):
        all_books = self.search([])
        books_sorted = self.sort_books_by_date(all_books)
        logger.info('Books before sorting: %s', all_books)
        logger.info('Books after sorting: %s', books_sorted)

    @api.model
    def sort_books_by_date(self, all_books):
        return all_books.sorted(key='date_release',reverse=True)
        ##return all_books.sorted(key='date_release')
    
     #######
   
   
   # obtencion de un conjunto de registros vacio para un modelo diferente
class LibraryMember(models.Model):

    _name = 'libreria.miembros'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Libreria de miembros"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Miembro desde..')
    date_end = fields.Date('Fecha de expiracion')
    member_number = fields.Char()
    date_of_birth = fields.Date('Fecha de naciminto')
#