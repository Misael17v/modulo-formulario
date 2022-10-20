from odoo import models,fields,api

class ResCompany(models.TransientModel):
    _name= 'wizard'
    
    date_from=fields.Datetime('Date from')
    date_to=fields.Datetime('date to')
    name_li=fields.Many2one('library.book',string="titulo")
    user_id=fields.Many2one('res.partner', string='usuario')
    
    #boton de imprimir, definimos una funcion,usamos un nombre para el boton imprimir que esta en wizard.xml el cual es:
    #<button name="check_report" string="Print" type="object" default_focus="1" class="oe_highlight" />
    # def check_report(self):
        #despues usamos data: aqui ponemos lo campos que definimos
          # data={'user_id':self.user_id,'date_from': self.date_from, 'date_to':self.date_to, 'name':self.name}
          #aqui es importante, ya que lo que esta en parentesis del ref(), 
          #lo va adentro es del id del primer record que esta en la carpeta view/report_wizard el cual es:action_report_wizard y
          # el my_library hace referencia a nuestro modulo que asi se llama
          #por lo que vamos a juntar esos 2 con un punto y debe quedar a unidos algo as: my_library.action_report_wizard
          
    def check_report(self):
        data = {}
        data['form'] = self.read(['user_id','name_li','date_from', 'date_to'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['user_id','name_li', 'date_from', 'date_to'])[0])
        return self.env.ref('my_library.action_report_wizard').report_action(self,data=data)
    
    
    