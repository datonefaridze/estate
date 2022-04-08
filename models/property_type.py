from odoo import fields, models
from odoo.exceptions import UserError

class EstateType(models.Model):
    _name = "estate.property.type"
    _description = "Test Model"
    name = fields.Char(required=True)
    sequence = fields.Integer('sequence', default=1, help="Used to order stages. Lower is better.")
    _order = "name"



#./odoo-bin --addons-path=../custom,../enterprise/,addons -d rd-demo -u estate
#./odoo-bin --addons-path=../custom,../enterprise/,addons -d rd-demo -u estate --dev xml



