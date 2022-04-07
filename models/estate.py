from odoo import fields, models
from odoo.exceptions import UserError

class EstateModel(models.Model):
    _name = "estate.property"
    _description = "Test Model"
    name = fields.Char(required=True)
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
    last_seen = fields.Datetime("Last Seen", default=lambda self: fields.Date.add(fields.Datetime.now(), months=3))  #fields.Datetime("Last Seen", default=lambda self: fields.Datetime.now())
    garden_orientation = fields.Selection([("n", "North"), ("s", "South"), ("w", "West"), ("e", "East")])
    active = fields.Boolean(active=False)
    state = fields.Selection([
        ('n', "New"),
        ('r', "Offer Received"),
        ('a', "Offer Accepted"),
        ('s', "Sold"),
        ('c', "Canceled"),
    ], required=True, copy=False, default="n")

    def action_sold(self):
        for record in self:
            if record.state == "sold":
                raise UserError("This Property has already been sold.")

            if record.state == "cancel":
                raise UserError("You cannot cancel a sold Property.")

            record.state = "sold"

        return True
#./odoo-bin --addons-path=../custom,../enterprise/,addons -d rd-demo -u estate
#./odoo-bin --addons-path=../custom,../enterprise/,addons -d rd-demo -u estate --dev xml




    # <record id="crm_lost_reason_view_form" model="ir.ui.view">
    #     <field name="name">estate.property.form</field>
    #     <field name="model">estate.property</field>
    #     <field name="arch" type="xml">
    #         <form string="Lost Reason">
    #             <sheet>
    #                 <div class="oe_button_box" name="button_box">
    #                     <button name="action_sold" type="object"
    #                         class="oe_stat_button" icon="fa-star">
    #                         <div class="o_stat_info">
    #                             <field name="postcode" class="o_stat_value"/>
    #                             <span class="o_stat_text"> Leads</span>
    #                         </div>
    #                     </button>
    #                 </div>
    #
    #                 <widget name="web_ribbon" title="Archived" bg_color="bg-danger" attrs="{'invisible': [('active', '=', True)]}"/>
    #                 <div class="oe_title">
    #                     <div class="oe_edit_only">
    #                         <label for="name"/>
    #                     </div>
    #                     <h1 class="mb32">
    #                         <newline>
    #                              <field name="name" class="mb16"/>
    #                             <field name="bedrooms" class="mb16"/>
    #                             <field name="living_area" class="mb16"/>
    #                         </newline>
    #
    #                         <field name="facades" class="mb16"/>
    #                         <field name="garage" class="mb16"/>
    #                     </h1>
    #                     <field name="active" invisible="1"/>
    #                 </div>
    #             </sheet>
    #         </form>
    #     </field>
    # </record>
