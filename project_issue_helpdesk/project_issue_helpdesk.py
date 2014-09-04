# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addons modules by CLEARCORP S.A.
#    Copyright (C) 2009-TODAY CLEARCORP S.A. (<http://clearcorp.co.cr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv,fields, orm
from openerp.tools.translate import _
import math

class ProjectIssue(osv.Model):
    _inherit = 'project.issue'
    
    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        list_branch={}
        result = super(ProjectIssue, self).onchange_partner_id(cr, uid, ids, partner_id)
        if partner_id:
            partner_obj=self.pool.get('res.partner')
            partner_ids=partner_obj.search(cr, uid,[('parent_id','=',partner_id),('partner_type','=','branch')])
            
            if not partner_ids:
                 result.update({'have_branch': False})
                 result.update({'branch_id':False})
            
            if partner_ids:                    
                 result.update({'have_branch': True})
        
        
        
        return {'value': result}
    
    #def _get_branch_id(self, cr, uid, ids,partner_id, arg, context=None):
    #    res={}
    #    partner_list=[]
    #    partner_obj=self.pool.get('res.partner')
    #    for issue in self.browse(cr, uid, ids, context=context):
    #        partner_ids=partner_obj.search(cr, uid,[('parent_id','=',issue.partner_id.id),('partner_type','=','branch')])
    #        if partner_ids:
    #            res[issue.id]=partner_ids
    #        else:
    #            res[issue.id]=None
    #    
    #    return res 

    
    def onchange_product_id(self, cr, uid, ids, product_id,context={}):
        data = {}
        if product_id:
            product = self.pool.get('product.product').browse(cr, uid, product_id, context)
            data.update({'categ_id': product.categ_id.id})

            prodlot_obj=self.pool.get('stock.production.lot')
            prodlot=prodlot_obj.search(cr, uid,[('product_id','=',product_id)])
            
            if not prodlot:
                data.update({'prodlot_id': False})
        return {'value': data}
    
    def onchange_categ_id(self, cr, uid,ids,categ_id,context={}):
            data={}
            
            product_obj=self.pool.get('product.product')
            product=product_obj.search(cr, uid,[('categ_id','=',categ_id)])

            if not product:
                data.update({'product_id': False})
                data.update({'prodlot_id': False})
                
            return {'value': data}
    
    _columns = {
                'issue_type': fields.selection([('support','Support'),('preventive check','Preventive Check'),
                                              ('workshop repair','Workshop Repair'),('installation','Installation')],
                                             required=True,string="Issue Type"),
                'warranty': fields.selection([('seller','Seller'),('manufacturer','Manufacturer')],string="Warranty"),                                 
                'backorder_ids': fields.one2many('stock.picking.out','issue_id'),
                'origin_id':fields.many2one('project.issue.origin',string="Origin"),
                'partner_type':fields.related('partner_id','partner_type',relation='res.partner',string="Partner Type"),
                'categ_id':fields.many2one('product.category',required=True,string="Category Product"),
                'product_id':fields.many2one('product.product',string="Product"),
                'prodlot_id':fields.many2one('stock.production.lot',string="Serial Number"),
                'branch_id':fields.many2one('res.partner', type='many2one', string='Branch'),
                'have_branch':fields.boolean(string="Have Branch")
                }
    
class ProjectIssueOrigin(osv.Model):
    _name = 'project.issue.origin'
    
    _columns = {
                'name': fields.char(required=True,string="Name"),
                'description': fields.text(string="Description")
                }

class HrAnaliticTimeSheet(osv.Model):
    _inherit = 'hr.analytic.timesheet'
    
    def _check_start_time(self, cr, uid, ids, context={}):
        hour=0.0
        min=0.0
        for timesheet_obj in self.browse(cr, uid, ids, context=context):
            if timesheet_obj.start_time:
                hour = math.floor(timesheet_obj.start_time)
                min = round((timesheet_obj.start_time % 1) * 60)
            if (hour not in range(0,24) or min not in range(0,60)):
                return False
        return True
    
    def _check_end_time(self, cr, uid, ids, context={}):
        hour=0.0
        min=0.0
        for timesheet_obj in self.browse(cr, uid, ids, context=context):
            if timesheet_obj.end_time:
                hour = math.floor(timesheet_obj.end_time)
                min = round((timesheet_obj.end_time % 1) * 60)
            if (hour not in range(0,24) or min not in range(0,60)):
                return False
        return True
    
    def _compute_duration(self, cr, uid, ids, field, arg, context=None):
        res = {}
        for timesheet_obj in self.browse(cr, uid, ids, context=context):
                res[timesheet_obj.id] = timesheet_obj.end_time-timesheet_obj.start_time
        return res
    
    _columns = {
                'ticket_number': fields.char(required=True,string="Ticket Number"),
                'start_time': fields.float(required=True,string="Start Time"),
                'end_time': fields.float(required=True,string="End Time"),
                'service_type': fields.selection([('expert','Expert'),('assistant','Assistant')],required=True,string="Service Type"),                       
                'unit_amount':fields.function(_compute_duration, type='float', string='Quantify',required=True,store=True)
                }
    
    _constraints = [
        (_check_start_time,'Format Start Time incorrect',['start_time']
         ),
         (_check_end_time,'Format End Time incorrect',['end_time']
         )]
     

class StockPicking(orm.Model):
    _inherit = 'stock.picking'

    _columns = {
         'issue_id': fields.many2one('project.issue')
    }

class StockPickingOut(orm.Model):
    _inherit = 'stock.picking.out'

    def __init__(self, pool, cr):
        super(StockPickingOut, self).__init__(pool, cr)
        self._columns['issue_id'] = self.pool['stock.picking']._columns['issue_id']
        
class ResPartner(orm.Model):
    _inherit = 'res.partner'
    
    def onchange_partner_type(self, cr, uid, ids,partner_type,context={}):
        res={}
        
        if partner_type=='company':
            res['is_company'] = True
        elif partner_type=='branch':
            res['is_company'] = False
        elif partner_type=='customer':
            res['is_company'] = False
        return {'value': res}
    
    _columns = {
        'partner_type': fields.selection([('company','Company'),('branch','Branch'),('customer','Customer')],required=True,string="Partner Type"),
        'provision_amount':fields.float(digits=(16,2),string="Provision Amount")
     }
    _defaults={
        'provision_amount':0.0
        }
    
class ContractPricelist(orm.Model):
    _name = 'contract.pricelist'

    _columns = {
        'name':fields.char(size=256,required=True,string="Name"),
        'account_analytic_id':fields.many2one('account.analytic.account',required=True,string="Account Analytic"),
        'partner_id':fields.related('account_analytic_id','partner_id',relation='res.partner',type='many2one',string="Partner"),
        'calendar_id':fields.many2one('resource.calendar',required=True,string="Calendar"),
        'line_ids': fields.one2many('contract.pricelist.line','contract_pricelist_id')
        }
    _sql_constraints = [
        ('account_analytic_unique',
        'UNIQUE(account_analytic_id)',
        'Account Analytic already exist ')
                        ]
    
class ContractPriceLine(orm.Model):
    _name = 'contract.pricelist.line'

    def onchange_pricelist_line_type(self, cr, uid, ids,pricelist_line_type,context={}):
        res={}
        
        if pricelist_line_type:
            if pricelist_line_type=='category':
                res['product_id'] = ""
            elif pricelist_line_type=='product':
                res['categ_id'] = ""
        elif not pricelist_line_type:
             res['product_id'] = ""
             res['categ_id'] = ""
        return {'value': res}
           
    def _check_lines(self, cr, uid, ids, context={}):
        if context is None:   
            context = {}
        for lines in self.browse(cr, uid, ids, context=context):
            if lines.pricelist_line_type=='category':
                exist_category = self.search(cr, uid, [('categ_id','=', lines.categ_id.id),('contract_pricelist_id','=', lines.contract_pricelist_id.id)])
                if len(exist_category)>1:
                    return False
            elif lines.pricelist_line_type=='product':
                exist_product = self.search(cr, uid, [('product_id','=', lines.product_id.id),('contract_pricelist_id','=', lines.contract_pricelist_id.id)])
                if len(exist_product)>1:
                    return False
        return True

    def _check_rates(self, cr, uid, ids, context={}):
        for rates in self.browse(cr, uid, ids, context=context):
            if (rates.technical_rate<1.0 or rates.assistant_rate<1.0):
                return False
        return True
    
    def _check_multipliers(self, cr, uid, ids, context={}):
        for multipliers in self.browse(cr, uid, ids, context=context):
            if (multipliers.overtime_multiplier<1.0 or multipliers.holiday_multiplier<1.0):
                return False
        return True
    
    _columns = {
        'contract_pricelist_id':fields.many2one('contract.pricelist',string="Contract Pricelist"),
        'pricelist_line_type': fields.selection([('category','Category'),('product','Product')],string="Pricelist Type"),                                 
        'categ_id':fields.many2one('product.category',string="Category Product"),
        'product_id':fields.many2one('product.product',string="Product"),
        'technical_rate':fields.float(digits=(16,2),required=True,string="Technical Rate"),
        'assistant_rate':fields.float(digits=(16,2),required=True,string="Assistant Rate"),
        'overtime_multiplier':fields.float(digits=(16,2),required=True,string="Overtime Multiplier"),
        'holiday_multiplier':fields.float(digits=(16,2),required=True,string="Holiday Multiplier")
       }
    
    _defaults={
        'technical_rate':0.0,
        'assistant_rate':0.0,
        'overtime_multiplier':1.0
        }
             
    _constraints = [
        (_check_lines,'Contract only allow a line to a single product o category',['categ_id','product_id']),
        (_check_rates,'Rates must be greater or equal to one',['technical_rate','assistant_rate']),
        (_check_multipliers,'Multipliers must be greater or equal to one',['overtime_multiplier','holiday_multiplier']) 
                ]
    #_sql_constraints = [
    #    ('contract_line_unique_category',
    #    'UNIQUE(contract_pricelist_id,category_id)',
    #    'Contract only allow a line to a single category'),
    #    ('contract_line_unique',
    #    'UNIQUE(contract_pricelist_id,product_id)',
    #    'Contract only allow a line to a single product')
    #]

class HolidayCalendar(orm.Model):
    _name = 'holiday.calendar'

    _columns = {
        'name':fields.char(size=256,required=True,string="Name"),
        'date':fields.date(required=True,string="Date"),
        'notes':fields.text(string="Notes")
        }
                        
class SaleOrder(osv.Model):
    _inherit = 'sale.order'
    
    def _project_exists(self, cr, user, ids, name, arg, context=None):
        res = {}
        for sale in self.browse(cr, user, ids, context=context):
            res[sale.id] = False
            if sale.project_id:
                res[sale.id] = True
        return res

    def action_button_create_project(self, cr, uid, ids, context=None):  
              
        context.update({'sale_order': ids})
        return {'type': 'ir.actions.act_window',
                'res_model': 'project.project',
                'view_type': 'form',
                'view_mode': 'form',
                'nodestroy': True,
                'target': 'current',  
                'flags': {'form': {'action_buttons': True}}
                }
       
    def action_button_view_project(self, cr, uid, ids, context=None):
        sale_order = self.browse(cr, uid, ids[0], context=context)
        return {'type': 'ir.actions.act_window',
                'res_model': 'project.project',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': sale_order.project_id.id,
                'nodestroy': True,
                'target': 'current',  
                'flags': {'form': {'action_buttons': False}}   
                }
    
    _columns = {
        'project_id':fields.many2one('project.project',string="Project"),
        'project_exists': fields.function(_project_exists, string='Project', type='boolean', help="It indicates that sales order has at least one project."),

        }
    
class Project(orm.Model):
    _inherit = 'project.project'
    
    def create(self, cr, uid, vals, context=None):
            new_project= super(Project, self).create(cr, uid, vals, context=context)
            if context.get('active_id'):
                sale_order_obj = self.pool.get('sale.order')
                sale_order_obj.write(cr, uid,[context.get('active_id')],{'project_id':new_project}, context=context)
            return new_project
         


                        