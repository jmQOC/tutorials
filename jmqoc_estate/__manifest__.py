{
    "name": "Real Estate",
    "version": "0.0",
    "author": "Jimmy McCann",
    "depends": ["base"],
    "application": True,  # so that the module appears when the ‘Apps’ filter is on,
    "data": [
        "security/ir.model.access.csv",
        "views/jmqoc_estate_property_views.xml",
        "views/jmqoc_estate_menus.xml",
    ],
}
