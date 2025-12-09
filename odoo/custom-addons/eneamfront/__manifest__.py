# -*- coding: utf-8 -*-
{
    'name': "eneamfront",

    'summary': "Pointage avec Back Django",

    'description': """
    I'll do that after
    """,

    'author': "Fenohery",
    'website': "https://fenohery-pf-00.vercel.app/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Employee',
    'version': '1.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'website', 'web', 'web_editor'],

    # always loaded
    'data': [
        # 1. modèle
        # 2. sécurité
        'security/security.xml',
        'security/ir.model.access.csv',
        # 3. Vues
        'views/hr_employee_views.xml',
        'views/page_dg_template.xml',
        'views/page_employe_template.xml',
        'views/templates.xml',
        # Donnée
        'data/menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'eneamfront/static/src/js/calendar_widget.js',
            'eneamfront/static/src/js/employe_widget.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto-install': False,
}
