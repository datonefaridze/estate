from odoo import fields, models
from odoo.exceptions import UserError

class EstateTag(models.Model):
    _name = "estate.property.tag"
    _description = "Test Model"
    name = fields.Char(required=True)
    _order = "name"
    _sql_constraints = [
        (
            "check_name",
            "UNIQUE(name)",
            "A property tag name and property type name must be unique",
        )
    ]
