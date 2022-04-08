from odoo import fields, models
from odoo.exceptions import UserError

class EstateType(models.Model):
    _name = "estate.property.type"
    _description = "Test Model"
    _order = "name"
    name = fields.Char(required=True)
    sequence = fields.Integer('sequence', default=1, help="Used to order stages. Lower is better.")






