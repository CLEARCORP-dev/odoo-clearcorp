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

from openerp.osv import fields, osv

class ProductInvoiceReport(osv.osv_memory):
    _name = "invoice.report.wiz"
      
    _columns = {
         'sortby':fields.selection([('sort_date', 'Date'), ('sort_period','Period'), ('sort_partner','Partner'),('sort_product','Product'),('sort_product_category','Product Category')], string="Sort by",required=True),
         'filter':fields.selection([('filter_no', 'No Filter'), ('filter_date','Date'), ('filter_period','Period')], string="Filter",required=True),
         'date_from': fields.date(string="Start Date"),
         'date_to': fields.date(string="End Date"),
         'fiscalyear_id':fields.many2one('account.fiscalyear',string="Fiscal Year"),
         'period_to': fields.many2one('account.period',string="End Period"),
         'period_from': fields.many2one('account.period',string="Start Period"),
         'partner_ids': fields.many2many('res.partner',string="Customer")   
        }  

    def _check_filter_date(self, cr, uid, ids, context={}):
        for wiz in self.browse(cr, uid, ids, context=context):
            if wiz.filter=='filter_date':
               if wiz.date_from>wiz.date_to:
                   return False
        return True
    
    def _check_filter_period(self, cr, uid, ids, context={}):
        for wiz in self.browse(cr, uid, ids, context=context):
            if wiz.filter=='filter_period':
               if wiz.period_from.date_start>wiz.period_to.date_stop:
                   return False
        return True
    
    
            
    _constraints = [
        (_check_filter_date,'Start Date must be less than End Date ',['date_from','date_to']
         ),
         (_check_filter_period,'Start Period must be less than End Period',['period_from','period_to']
         )]  
    
    
    def _print_report(self, cursor, uid, ids, datas, context=None):
        context = context or {}
       
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'product_invoice_report',
            'datas': datas}

    def action_validate(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        datas = {}
        datas['ids'] = context.get('active_ids', [])
        datas['model'] = context.get('active_model', 'ir.ui.menu')
        datas['form'] = self.read(cr, uid, ids, ['sortby',  'filter', 'date_from','date_to','period_to','period_from','fiscalyear_id','partner_ids'], context=context)[0]
        return self._print_report(cr, uid, ids, datas, context=context)

        
