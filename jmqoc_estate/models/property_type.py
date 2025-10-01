from odoo import fields, models


class PropertyType(models.Model):

    _name = "jmqoc.estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char("Type", required=True)
