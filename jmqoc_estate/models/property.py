from odoo import api, fields, models
from odoo.tools import date_utils

import logging


_logger = logging.getLogger(__name__)


class Property(models.Model):
    _name = "jmqoc.estate.property"
    _description = "Real Estate Property"

    name = fields.Char("Title", required=True)

    active = fields.Boolean("Is Active", default=True)

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer-received", "Offer Received"),
            ("offer-accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )

    # So Gemini lied to me, you cannot do dynamic selections like I had before.
    # It would likely require an additional static model with the categories for each property type.
    # Probably close to how states and countries work
    # property_type = fields.Selection(
    #    [
    #        ("residential", "Residential"),
    #        ("single-family", "Single-Family Home"),
    #        ("condo", "Condo"),
    #        ("townhouse", "Townhouse"),
    #        ("multi-family", "Multi-Family House"),
    #        ("commercial", "Commercial"),
    #        ("industrial", "Industrial"),
    #        ("land", "Land"),
    #   ],
    #    string="Property Type",
    #    default="residential",
    #    required=True,
    # )

    property_type_id = fields.Many2one(
        "jmqoc.estate.property.type", string="Property Type"
    )

    property_tag_ids = fields.Many2many("jmqoc.estate.property.tag", string="Tags")

    description = fields.Char("Description")

    street_address = fields.Char("Street Address", required=True)

    city = fields.Char("City", required=True)

    state_id = fields.Many2one(
        "res.country.state", string="State", domain="[('country_id', '=', country_id)]"
    )

    postal_code = fields.Char("Postcode", required=True)

    country_id = fields.Many2one(
        "res.country",
        string="Country",
        default=lambda self: self.env["res.country"]
        .search([("name", "=", "United States")], limit=1)
        .id,
    )

    bedrooms = fields.Integer("Number of Bedrooms", default=2)

    living_area = fields.Integer("Living Area (sq ft)")

    facades = fields.Integer("Number of Facades")

    garage = fields.Boolean("Has Garage")

    garden = fields.Boolean("Has Garden")

    @api.onchange("garden")
    def _onchange_garden(self):
        # because of the onchange decorator, self now represents the current record in the form view
        _logger.info(f"Garden status for {self.name} changed to {self.garden}")
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    garden_area = fields.Integer("Garden Area (sq ft)")

    garden_orientation = fields.Selection(
        [("north", "North"), ("east", "East"), ("south", "South"), ("west", "West")],
        string="Garden Orientation",
    )

    total_area = fields.Integer("Total Area (sq ft)", compute="_total_area")

    @api.depends("living_area", "garden_area")
    def _total_area(self):
        # self is a collection, a recordset, of all the records for this particular model
        for property in self:
            _logger.info(f"Computing total area for property '{property.name}'")
            property.total_area = property.living_area + property.garden_area

    date_available = fields.Date(
        "Date Available",
        copy=False,
        default=date_utils.add(fields.Date.today(), months=3),
    )

    expected_price = fields.Float("Expected Price", (10, 2), required=True)

    selling_price = fields.Float("Selling Price", (10, 2), readonly=True, copy=False)

    user_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.uid
    )

    offer_ids = fields.One2many(
        "jmqoc.estate.property.offer", "property_id", string="Offers"
    )

    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
