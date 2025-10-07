from odoo import fields, models


class User(models.Model):

    _inherit = "res.users"

    property_ids = fields.One2many(
        "jmqoc.estate.property",
        "user_id",
        string="Available Properties",
        domain=[
            ("date_available", "<=", fields.Date.today()),
            ("state", "in", ["new", "offer-received"]),
        ],
    )
