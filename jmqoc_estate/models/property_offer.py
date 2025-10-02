from odoo import api, fields, models
from odoo.tools import date_utils

import logging

_logger = logging.getLogger(__name__)


class PropertyOffer(models.Model):

    _name = "jmqoc.estate.property.offer"
    _description = "Real Estate Purchase Offer on a Property"

    property_id = fields.Many2one("jmqoc.estate.property", string="On Property")

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    price = fields.Float("Offer Amount")

    validity = fields.Integer("Valid for (days)", default=7)

    deadline = fields.Date("Decision Due", compute="_deadline", inverse="_validity")
    # the inverse method is called when saving the record, while the compute method is called at each change of its dependencies.

    @api.depends("create_date", "validity")
    def _deadline(self):
        # self is a collection, a recordset, of all the records for this particular model
        for offer in self:
            offer_create_date = offer.create_date or fields.Date.today()
            _logger.info(
                f"Fetched create date of {offer_create_date} for offer on {offer.property_id.name} from {offer.partner_id.name} for calculating deadline"
            )
            offer.deadline = date_utils.add(offer_create_date, days=offer.validity)

    def _validity(self):
        for offer in self:
            offer_create_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            _logger.info(
                f"Fetched create date of {offer_create_date} for offer on {offer.property_id.name} from {offer.partner_id.name} for calculating validity"
            )
            offer.validity = (offer.deadline - offer_create_date).days

    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
