from odoo import api, fields, models
from odoo.exceptions import UserError
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

    def update_status(self):
        to_status = self.env.context.get("to_status")
        possible_statuses: list = [
            s[0]
            for s in self.env["jmqoc.estate.property.offer"]
            ._fields["status"]
            .selection  # pyright: ignore
        ]
        # Always assume that a method can be called on multiple records
        for offer in self:
            _logger.info(
                f"Received request to update status of offer from {offer.partner_id.name} on {offer.property_id.name} to {to_status}"
            )

            if offer.status == "accepted" and to_status == "refused":
                raise UserError("Accepted offers can not be refused")
            if offer.status == "refused" and to_status == "accepted":
                raise UserError("Refused offers can not be accepted")

            if offer.property_id.state == "offer-accepted" and to_status == "accepted":
                raise UserError(
                    "Can not accept an offer on a property with an 'Offer Accepted' status"
                )

            if to_status == "accepted" and "accepted" in [
                o.status for o in offer.property_id.offer_ids
            ]:
                raise UserError(
                    "Can not accept additional offers on a property with an already accepted offer"
                )

            if to_status not in possible_statuses:
                raise UserError(f"{to_status} is not a valid status for an Offer")

            offer.status = to_status
            if to_status == "accepted":
                offer.property_id.state = "offer-accepted"
                offer.property_id.selling_price = offer.price
                offer.property_id.partner_id = offer.partner_id

        return True
