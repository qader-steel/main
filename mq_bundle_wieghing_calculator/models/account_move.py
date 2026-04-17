from odoo import models, fields, api

class AccountMoveLine(models.Model):
    """
    Inherited to handle bundle quantities and delivered quantity computation in invoices.
    """
    _inherit = 'account.move.line'

    mq_bundle_qty = fields.Float(string="Bundle Qty.", digits='Product Unit of Measure')
    mq_quantity = fields.Float(string="Quantity", digits='Product Unit of Measure')

    @api.onchange('mq_quantity')
    def _onchange_mq_quantity(self):
        for line in self:
            line.quantity = line.mq_quantity

    @api.onchange('quantity')
    def _onchange_quantity_base(self):
        for line in self:
            if line.quantity != line.mq_quantity:
                line.mq_quantity = line.quantity

    mq_qty_delivered = fields.Float(string="Delivered", compute="_compute_mq_qty_delivered", digits='Product Unit of Measure')

    @api.depends('sale_line_ids.qty_delivered')
    def _compute_mq_qty_delivered(self):
        for line in self:
            line.mq_qty_delivered = sum(line.sale_line_ids.mapped('qty_delivered')) if line.sale_line_ids else 0.0

class AccountMove(models.Model):
    """
    Inherited to compute total bundle quantity and total weight for invoices.
    """
    _inherit = 'account.move'

    mq_total_bundle_qty = fields.Float(string="Total Bundle Qty.", compute="_compute_mq_totals", store=True)
    mq_total_weight = fields.Float(string="Total Weight (Ton)", compute="_compute_mq_totals", store=True)

    @api.depends('invoice_line_ids.mq_bundle_qty', 'invoice_line_ids.sale_line_ids')
    def _compute_mq_totals(self):
        for move in self:
            total_bundle = sum(move.invoice_line_ids.mapped('mq_bundle_qty'))
            
            # Fetch total weight from associated sale orders if they exist
            sale_orders = move.invoice_line_ids.mapped('sale_line_ids.order_id')
            if sale_orders:
                total_weight = sum(sale_orders.mapped('mq_total_weight'))
            else:
                total_weight = 0.0

            move.mq_total_bundle_qty = total_bundle
            move.mq_total_weight = total_weight
