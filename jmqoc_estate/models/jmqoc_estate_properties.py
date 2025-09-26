from odoo import fields, models, api


class Property(models.Model):
    _name = "jmqoc.estate.property"
    _description = "Real Estate Property"

    name = fields.Char("Property Name", required=True)

    property_type = fields.Selection(
        [
            ("residential", "Residential"),
            ("commercial", "Commercial"),
            ("industrial", "Industrial"),
            ("land", "Land"),
        ],
        string="Property Type",
        default="residential",
        required=True,
    )

    category = fields.Selection(
        selection="_get_property_categories", string="Property Category", required=False
    )

    street_address = fields.Char("Street Address", required=True)

    city = fields.Char("City", required=True)

    state_id = fields.Many2one(
        "res.country.state", string="State", domain="[('country_id', '=', country_id)]"
    )

    postal_code = fields.Char("Postal Code", required=True)

    country_id = fields.Many2one("res.country", string="Country")

    date_available = fields.Date("Date Available")

    expected_price = fields.Float("Expected Price", (10, 2), required=True)

    selling_price = fields.Float("Selling Price", (10, 2))

    bedrooms = fields.Integer("Number of Bedrooms")

    living_area = fields.Integer("Living Area (sq ft)")

    facades = fields.Integer("Number of Facades")

    garage = fields.Boolean("Has Garage")

    garden = fields.Boolean("Has Garden")

    garden_area = fields.Integer("Garden Area (sq ft)")

    garden_orientation = fields.Selection(
        [("north", "North"), ("east", "East"), ("south", "South"), ("west", "West")],
        string="Garden Orientation",
    )

    @api.depends("property_type")  # ensures the method runs when parent_field changes
    def _get_property_categories(self):
        if self.property_type == "residential":
            return [
                ("single-family", "Single-Family Home"),
                ("condo", "Condo"),
                ("townhouse", "Townhouse"),
                ("multi-family", "Multi-Family House"),
            ]
        return []
