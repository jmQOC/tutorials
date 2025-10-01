{
    "name": "Real Estate",
    "version": "0.0",
    "author": "Jimmy McCann",
    "depends": ["base"],
    "application": True,  # so that the module appears when the ‘Apps’ filter is on,
    "data": [
        "security/ir.model.access.csv",
        "views/property_offer.xml",
        "views/property.xml",
        "views/property_tag.xml",
        "views/property_type.xml",
        "views/menus.xml",
    ],
}
