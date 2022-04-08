from odoo import api, fields, models
from odoo.exceptions import UserError

class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Test Model"
    _order = "id desc"
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "The expected price must be stricly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The expected selling price must be positive.",
        ),
    ]

    name = fields.Char(required=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    user_ids = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_ids = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="tags_ids")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2, )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Date.add(fields.Datetime.now(), months=3))
    garden_orientation = fields.Selection([("n", "North"), ("s", "South"), ("w", "West"), ("e", "East")])
    active = fields.Boolean(active=False)
    state = fields.Selection([
        ('n', "New"),
        ('r', "Offer Received"),
        ('a', "Offer Accepted"),
        ('s', "Sold"),
        ('c', "Canceled"),
    ], required=True, copy=False, default="n")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price", "garden_area")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices, default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = None

    def action_sold(self):
        # print("PARENT ACTION SOLD")
        for record in self:
            if record.state == "s":
                raise UserError("This is sold property!!!")
            if record.state == "c":
                raise UserError("You can't cancel this property")
            record.state = "s"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "s":
                raise UserError("You can't sell sold property")
            if record.state == "c":
                raise UserError("This Property has been cancelled")
            record.state = "c"
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        for record in self:
            if record.state not in ["o", "c"]:
                raise UserError("Only new and canceled properties can be deleted.")


#./odoo-bin --addons-path=../custom,../enterprise/,addons -d rd-demo -u estate --dev xml



