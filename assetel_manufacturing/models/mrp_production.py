# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def button_mark_done(self):
        result = super(MrpProduction, self).button_mark_done()
        

        for line in self.move_raw_ids:
            if line.product_id.type == 'consu':
                move_lines = [
                            (0, 0, {
                                'account_id' : line.product_id.categ_id.property_stock_valuation_account_id.id,
                                'name': self.name +  ' - ' + line.product_id.name,
                                'credit': line.product_id.standard_price * line.quantity_done,
                            }),
                            (0, 0, {
                                'account_id' : line.product_id.property_stock_production.valuation_in_account_id.id,
                                'name': self.name +  ' - ' + line.product_id.name,
                                'debit': line.product_id.standard_price * line.quantity_done,
                            })
                        ]
                values = {
                    'ref' : self.name +  ' - ' + line.product_id.name,
                    'date' : self.write_date,
                    'journal_id' : line.product_id.categ_id.property_stock_journal.id,
                    'line_ids' : move_lines
                    }
                asiento = self.env['account.move'].create(values)
                asiento.action_post()
            
        return result


