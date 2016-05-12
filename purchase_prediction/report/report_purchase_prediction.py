# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from report import report_sxw


class purchase_prediction(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(collection_day, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })
report_sxw.report_sxw('report.purchase.prediction', 'purchase.prediction', 'addons/purchase_prediction/report/report_purchase_prediction.rml', parser=collection_day, header="external")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
