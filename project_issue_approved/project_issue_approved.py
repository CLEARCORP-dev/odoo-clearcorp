from openerp import models, fields, api

class feature(models.Model):
    
    _inherit = 'project.scrum.feature'
    
    """def write(self):
        approval_obj = self.env['account.analytic.prepaid_hours_approval']
        self.env['project.issue'].search([('','=',self.id)])
        if self.state == "quoted" and self.:
            approval_vals:{
                           
                           }"""
            

class issue(models.Model):
    
    _inherit = 'project.issue'
    
    group_approved = fields.One2many('account.analytic.prepaid_hours_approval','ticket_id')
    
    @api.model
    def fields_view_get(self,view_id=None, view_type='form', toolbar=False, submenu=False):

        if self._context is None:
            self._context = {}
        res = super(issue, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,submenu=False)
        record_id = self._context and self._context.get('active_id', False) or False
        active_model = self._context.get('active_model')
        if not view_type == 'form' or not record_id or (active_model and active_model != 'project.issue'):
            return res
        
        return res