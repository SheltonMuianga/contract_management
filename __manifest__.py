# Copyright 2022-Today sheltonmuianga.
{
    'name': "Contract Management Procurement",
    'version': "2.4",
    'description': """Module for Contract Management Procurement""",
    'summary': "Contract Management",
    'author': 'Shelton Muianga',
    'category': 'Industry',
    'website': "",
    'depends': ['mail','base'],
    'data': [
        # data
        'data/contract_management_data.xml',
        # Security
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        # wizards
        
        # Views
        'views/contract_views.xml',
        'views/contract_managements_views.xml',
        
        # Web Template
        # report
      
        # data
        
        # Menus
        'views/menus.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         'tk_insurance_management/static/src/css/theme.css',
    #         'tk_insurance_management/static/src/js/other/script.js',
    #     ],
    #     'web.assets_backend': [
    #         'tk_insurance_management/static/src/xml/template.xml',
    #         'tk_insurance_management/static/src/scss/style.scss',
    #         'tk_insurance_management/static/src/js/lib/apexcharts.js',
    #         'tk_insurance_management/static/src/js/dashboard/insurance_dashboard.js',
    #     ],
    # },
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'license': 'OPL-1',
    # 'price': 99,
    'currency': 'MZN'
}
