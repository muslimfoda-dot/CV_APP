from odoo import models,fields,api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _action_done(self):
        res = super(StockPicking, self)._action_done()
        for picking in self:
            sale_order = picking.sale_id
            if sale_order:
                invoices = sale_order._create_invoices(final=True)
                invoices.action_post()

    def _action_merge_pickings(self):
        """دمج أوامر استلام متعددة لنفس العميل"""
        if len(self) < 2:
            raise UserError(("يجب اختيار أمرين على الأقل للدمج"))

        # التحقق من أن جميع الأوامر لنفس العميل
        partners = self.mapped('partner_id')
        if len(partners) > 1:
            raise UserError(("لا يمكن دمج أوامر استلام لعملاء مختلفين"))

        # التحقق من نفس نوع العملية
        picking_types = self.mapped('picking_type_id')
        if len(picking_types) > 1:
            raise UserError(("لا يمكن دمج أوامر استلام من أنواع مختلفة"))

        # التحقق من نفس المخزن
        locations = self.mapped('location_dest_id')
        if len(locations) > 1:
            raise UserError(("لا يمكن دمج أوامر استلام لمخازن مختلفة"))

        # إنشاء أمر استلام جديد
        new_picking = self[0].copy({
            'origin': ', '.join(self.mapped('origin')),
            'move_ids': [],
        })

        # دمج بنود المنتجات
        moves_to_merge = []
        for picking in self:
            for move in picking.move_ids_without_package:
                existing_move = new_picking.move_ids_without_package.filtered(
                    lambda m: m.product_id == move.product_id
                              and m.location_id == move.location_id
                              and m.location_dest_id == move.location_dest_id
                )

                if existing_move:
                    # زيادة الكمية إذا كان المنتج موجوداً
                    existing_move.product_uom_qty += move.product_uom_qty
                else:
                    # نسخ البند إلى الأمر الجديد
                    move.copy({
                        'picking_id': new_picking.id,
                        'state': 'draft',
                    })

            # إلغاء الأمر القديم
            picking.action_cancel()

        # تحديث الكميات المحجوزة
        new_picking.action_assign()

        # فتح الأمر المدمج
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'res_id': new_picking.id,
            'view_mode': 'form',
            'target': 'current',
        }





