from odoo import api, fields, models

# --- History Dictionary Models ---
class MQDriverName(models.Model):
    _name = "mq.driver.name"
    _description = "Driver Name History"
    name = fields.Char(string="Driver Name", required=True)

class MQDriverPhone(models.Model):
    _name = "mq.driver.phone"
    _description = "Driver Phone History"
    name = fields.Char(string="Phone Number", required=True)

class MQCarPlate(models.Model):
    _name = "mq.car.plate"
    _description = "Car Plate History"
    name = fields.Char(string="Car Plate No.", required=True)

class MQBorderCrossing(models.Model):
    _name = "mq.border.crossing"
    _description = "Border Crossing History"
    name = fields.Char(string="Border Crossing", required=True)

class MQScaleNo(models.Model):
    _name = "mq.scale.no"
    _description = "Scale No History"
    name = fields.Char(string="Scale No.", required=True)


# --- Document Models ---
class SaleOrder(models.Model):
    _inherit = "sale.order"

    driver_name_id = fields.Many2one("mq.driver.name", string="Driver Name")
    driver_phone_id = fields.Many2one("mq.driver.phone", string="Driver Phone No.")
    car_plate_id = fields.Many2one("mq.car.plate", string="Car Plate No.")
    border_crossing_id = fields.Many2one("mq.border.crossing", string="Border Crossing")
    scale_no_id = fields.Many2one("mq.scale.no", string="Scale No.")


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # Delivery simply inherits from the Sale Order identically
    driver_name_id = fields.Many2one("mq.driver.name", string="Driver Name", related="sale_id.driver_name_id", readonly=False)
    driver_phone_id = fields.Many2one("mq.driver.phone", string="Driver Phone No.", related="sale_id.driver_phone_id", readonly=False)
    car_plate_id = fields.Many2one("mq.car.plate", string="Car Plate No.", related="sale_id.car_plate_id", readonly=False)
    border_crossing_id = fields.Many2one("mq.border.crossing", string="Border Crossing", related="sale_id.border_crossing_id", readonly=False)
    scale_no_id = fields.Many2one("mq.scale.no", string="Scale No.", related="sale_id.scale_no_id", readonly=False)


class AccountMove(models.Model):
    _inherit = "account.move"

    sale_order_ids = fields.Many2many(
        comodel_name="sale.order",
        compute="_compute_sale_order_ids",
        string="Related Sales Orders"
    )
    
    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        compute="_compute_sale_order_ids",
        store=True,
        string="Source Sales Order",
    )

    # Invoice simply inherits from the Sale Order identically
    driver_name_id = fields.Many2one("mq.driver.name", string="Driver Name", related="sale_order_id.driver_name_id", readonly=False)
    driver_phone_id = fields.Many2one("mq.driver.phone", string="Driver Phone No.", related="sale_order_id.driver_phone_id", readonly=False)
    car_plate_id = fields.Many2one("mq.car.plate", string="Car Plate No.", related="sale_order_id.car_plate_id", readonly=False)
    border_crossing_id = fields.Many2one("mq.border.crossing", string="Border Crossing", related="sale_order_id.border_crossing_id", readonly=False)
    scale_no_id = fields.Many2one("mq.scale.no", string="Scale No.", related="sale_order_id.scale_no_id", readonly=False)

    @api.depends("invoice_line_ids.sale_line_ids.order_id")
    def _compute_sale_order_ids(self):
        for move in self:
            orders = move.invoice_line_ids.mapped('sale_line_ids.order_id')
            move.sale_order_ids = orders
            move.sale_order_id = orders[0] if orders else False
