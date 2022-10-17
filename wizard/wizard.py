from odoo import models,fields,api

class ResCompany(models.TransientModel):
    _name= 'wizard'
    
    date_from=fields.Date()
    date_to=fields.Date()
    name=fields.Char()
    
    
    def check_report(self):
        data = {'date_from': self.date_from, 'date_to':self.date_to, 'name':self.name}
        data['form'] = self.read(['name', 'date_from', 'date_to'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['name', 'date_from', 'date_to'])[0])
        return self.env['report'].get_action(self, 'my_library.wizard_pdf_template', data=data) 
    
    ##este el el boton imbrimir o print
#     def action_print_report(self):
#         data={'date_from': self.date_from, 'date_to':self.date_to, 'name':self.name}
#         return self.env.ref('my_library.wizard_report.xml').report_action(self,data=data)
    
# class   WizardReportPDF(models.AbstractModel):
#      _name = 'report.my_library.my_library_pdf_template'

#      def _get_report_values(self, docids, data=None):
#          domain = [('state', '!=', 'cancel')]
#          if data.get('date_from'):
#              domain.append(('course_date', '>=', data.get('date_from')))
#          if data.get('date_to'):
#              domain.append(('course_date', '<=', data.get('date_to')))
#          if data.get('name'):
#              domain.append(('id', 'in', data.get('name')))
             
#          docs = self.env['library.book.category'].search(domain)
#          responsible = self.env['res.users'].browse(data.get('responsible_id'))
#          course_ids = self.env['library.book.category'].browse(data.get('course_ids'))
#          data.update({'responsbile': responsible.name})
#          data.update({'courses': ",".join([course.course_name for course in course_ids])})
#          print(docs)
#          print(data)
#          return {
#              'doc_ids': docs.ids,
#              'doc_model': 'openacademy.course',
#              'docs': docs,
#              'datas': data
#          }

