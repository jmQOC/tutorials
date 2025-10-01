from odoo import fields, models


class PropertyOffer(models.Model):

    _name = "jmqoc.estate.property.offer"
    _description = "Real Estate Purchase Offer on a Property"

    property_id = fields.Many2one("jmqoc.estate.property", string="On Property")

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    price = fields.Float("Offer Amount")

    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
