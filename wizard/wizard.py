from odoo import models,fields,api

class ResCompany(models.TransientModel):
    _name= 'wizard'
    
    date_from=fields.Date('Fecha inicial')
    date_to=fields.Date('Fecha final')
    name_li=fields.Many2one('library.book',string="Codigo")
    user_id=fields.Many2one('res.partner', string='Factura')
    
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
        domain=[]
        user_id = self.user_id
        if user_id:
            domain += [('user_id','=', user_id[0])]
        date_from= self.date_from
        if date_from:
            domain += [('date_release','>=', date_from)]
        date_to= self.date_to
        if date_to:
            domain += [('date_release','<=', date_to)]
            print("domain",domain)
        
        print("test...", self.read()[0])
        busqueda =self.env['library.book'].search_read()
        data = {
            'form': self.read()[0],
            'busqueda':busqueda
        }
        # data['form'] = self.read(['user_id','name_li','date_from', 'date_to'])[0]
        # data['busqueda'] = self.read(['busqueda'])
        # return self._print_report(data)

    # def _print_report(self, data):
    #     data['form'].update(self.read(['user_id','name_li', 'date_from', 'date_to'])[0])
        return self.env.ref('my_library.action_report_wizard').report_action(self,data=data)
    
    
    