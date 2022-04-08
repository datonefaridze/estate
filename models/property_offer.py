from odoo import fields, models, api
from odoo.exceptions import UserError
import datetime
from odoo.tools import float_compare


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Test Model"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "An offer price must be strictly positive")
    ]
    name = fields.Char()
    price = fields.Float()
    status = fields.Selection([("a", "Accepted"),
                               ("r", "Refused"),
                               ])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline",
        compute="_compute_deadline",
        readonly=False,
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            date = (
                record.create_date.date()
                if record.create_date
                else datetime.date.today()
            )
            record.date_deadline = date + datetime.timedelta(days=record.validity)

    @api.onchange("date_deadline")
    def _inverse_compute_deadline(self):
        for record in self:
            date = (
                record.create_date.date()
                if record.create_date
                else datetime.date.today()
            )
            record.validity = (record.date_deadline - date).days

    def action_accept(self):
        for record in self:
            if record.status is not False:
                raise UserError(
                    f"You cannot accept an offer has already been {record.status}."
                )
            record.status = "a"
            record.property_id.buyer_ids = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            if record.status is not False:
                raise UserError(
                    f"You cannot refuse an offer has already been {record.status}."
                )
            record.status = "r"
        return True

    @api.constrains("price")
    def _check_price(self):
        for record in self:
            record.check_price()

    def check_price(self):
        max_price = self.property_id.expected_price * 0.9
        if float_compare(self.price, max_price, precision_digits=2) == -1:
            raise ValidationError(
                "The selling price cannot be lower than 90% of the expected price"
            )