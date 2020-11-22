{
    "name": "g_glass",
    "version": '0.0.0',
    "license": "LGPL-3",
    "author": "g_glass",
    "website": "https://www.g_glass.at",
    "depends": [
        "base",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/views_commande.xml",
        "views/views_facteur.xml",
        "views/views_operation.xml",
        # "views/views_service.xml",

    ],
    "images": [
        'static/img/glass.png'
    ],
    "sequence": 3,
    "application": True,
    "installable": True,
    "auto_install": True,
}
