# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from datetime import datetime
from osv import fields, osv
from tools.translate import _


class product_supplierinfo(osv.osv):
    _inherit = "product.supplierinfo"
    _columns = {
        'product_id': fields.many2one('product.product', 'Product', required=True)
    }


class purchase_prediction_line(osv.osv):
    _name = "purchase.prediction.line"
    _columns = {
        'name': fields.char('Nombre',size=64,readonly=True),
        'product_id' : fields.many2one('product.product', 'Product',readonly=True),
        'qty_sold': fields.float('Cantidad Vendidas', readonly=True),
        'qty_purchase': fields.float('Cantidad Compradas', readonly=True),
        'qty_proyect': fields.float('Cantidad Proyectos', readonly=True),
        'stock_available':fields.related('product_id','qty_available',type='float',string='Real Stock', store=False, readonly=True),
        'virtual_available':fields.related('product_id','virtual_available',type='float',string='Virtual Stock', store=False, readonly=True),
        'qty_approved': fields.float('Cantidad Recomendada'),
        'prediction_id' : fields.many2one('purchase.prediction', 'Prediction'),
    }


class purchase_prediction(osv.osv):
    def create(self, cr, uid, vals, context=None):
        vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'purchase.prediction')
        res = super(purchase_prediction, self).create(cr, uid, vals, context=context)

        #~ Instances
        prod_list = []
        prod_id_list = []
        stock_picking_in_list = []
        stock_picking_out_list = []
        stock_picking_int_list = []

        prod_obj = self.pool.get('product.product')
        stock_picking_obj = self.pool.get('stock.picking')
        stock_move_obj = self.pool.get('stock.move')
        prediction_line_obj = self.pool.get('purchase.prediction.line')
        supplier_info_obj = self.pool.get('product.supplierinfo')
        start_month =  datetime.strptime(vals['start_date'],'%Y-%m-%d')
        end_month = datetime.strptime(vals['end_date'],'%Y-%m-%d')
        
        if start_month >= end_month:
            raise osv.except_osv(_('Warning !'), _('Revise las fechas de inicio y fin.'))
        
        months_qty = (end_month.year - start_month.year) * 12 + end_month.month - start_month.month
        
        supplier_info_list = supplier_info_obj.search(cr, uid, [('name','=',vals['partner_id'])], context=context)
        stock_picking_in_list = stock_picking_obj.search(cr, uid, [('date','>=',vals['start_date']),('date','<=',vals['end_date']),('type','=','in'),('state','=','done')], context=context)
        stock_picking_out_list = stock_picking_obj.search(cr, uid, [('date','>=',vals['start_date']),('date','<=',vals['end_date']),('type','=','out'),('state','=','done')], context=context)
        stock_picking_int_list = stock_picking_obj.search(cr, uid, [('date','>=',vals['start_date']),('date','<=',vals['end_date']),('type','=','internal'),('state','=','done')], context=context)

        for supplier_info in supplier_info_obj.browse(cr, uid, supplier_info_list, context=context):
            prod_list.append(supplier_info.product_id)
               
        for product in prod_list:

            # Si el product_id en la tabla product_supplierinfo no es el 
            # id de la tabla product_product entonces es el product_tpml_id
            # por lo tanto buscamos el producto por el product_tpml_id
            # para que la busqueda no de un error
            try:
                logging.getLogger("Name").info(product.name)
            except:
                p_id = prod_obj.search(cr, uid, [('product_tmpl_id','=', product.id),], context=context)
                p = prod_obj.browse(cr, uid, p_id, context=context)
                product = p[0]
            

            qty_approved = 0
            qty_purchase = 0
            qty_sold = 0
            qty_proyect = 0
            stock_move_in_list = []
            stock_move_out_list = []
            stock_move_int_list = []

            stock_move_in_list = stock_move_obj.search(cr, uid, [('state','=','done'),('product_id','=',product.id),('picking_id','in',stock_picking_in_list),('date','>=',vals['start_date']),('date','<=',vals['end_date'])], context=context)
            stock_move_out_list = stock_move_obj.search(cr, uid, [('state','=','done'),('product_id','=',product.id),('picking_id','in',stock_picking_out_list),('date','>=',vals['start_date']),('date','<=',vals['end_date'])], context=context)
            stock_move_int_list = stock_move_obj.search(cr, uid, [('state','=','done'),('product_id','=',product.id),('picking_id','in',stock_picking_int_list),('date','>=',vals['start_date']),('date','<=',vals['end_date'])], context=context)

            # Purchase qty
            for move in stock_move_obj.browse(cr, uid, stock_move_in_list, context=context):
                qty_purchase = qty_purchase + move.product_qty

            # Sold qty
            for move in stock_move_obj.browse(cr, uid, stock_move_out_list, context=context):
                qty_sold = qty_sold + move.product_qty

            # Used in MRP Production
            for move in stock_move_obj.browse(cr, uid, stock_move_int_list, context=context):
                qty_proyect = qty_proyect + move.product_qty
            
            try:
                if product.virtual_available < product.qty_available:
                    qty_approved = ((qty_sold + qty_proyect - product.qty_available) / months_qty) * vals['prediction_month_qty']           
                else:
                    qty_approved = ((qty_sold + qty_proyect - product.virtual_available) / months_qty) * vals['prediction_month_qty']
            except:
                qty_approved = 0
            
            data = {
            'product_id': product.id,
            'name': self.pool.get('ir.sequence').get(cr, uid, 'purchase.prediction'),
            'qty_sold' : qty_sold,
            'qty_purchase': qty_purchase,
            'qty_proyect': qty_proyect,
            'qty_approved': qty_approved,
            'prediction_id': res
            }
            
            prediction_line_obj.create(cr,uid,data)

        return res

    _name = "purchase.prediction"
    _columns = {
        'name': fields.char('Nombre',size=64,readonly=True),
        'partner_id' : fields.many2one('res.partner', 'Supplier',required=True),
        'prediction_month_qty': fields.float('Cantidad Meses'),
        'prediction_id' : fields.one2many('purchase.prediction.line','prediction_id', 'Products'),
        'start_date' : fields.date('Fecha Inicio', required=True),
        'end_date' : fields.date('Fecha Fin', required=True),
        'create_date' : fields.datetime('Fecha Creacion', readonly=True),
    }
