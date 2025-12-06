{
    'name': "app one",
    'author': "muslim foda",
    'category': "",
    'version': '18.0.0.1.0',
    'depends': [
        'mail',
        'base',
        'web',
        'contacts',
        'sale_management',
        'account',
        'stock',
        'sale_stock',


    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menus_views.xml',
        'views/res_partner_views.xml',
             'views/sale_order.xml',
             'views/cv_app_views.xml',
             'views/owner_views.xml',
             'views/tag_views.xml',
        'views/reserved_field_views.xml',
        'views/cv_app_history.xml',
        'wizard/change_state_wizard_view.xml',
        'reports/cv_app_report.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'app_one/static/src/css/cv_app.css',
        ],
    },
    'application': True,
}
