# -*- coding: utf-8 -*-
{
    'name': "opros",
    'summary': """Опрос""",
    'description': """Голосование за лучшее название университета!""",
    'author': "Anastasia Tomilina, Anton Goroshkin",
    'website': "www.sibsau.ru",
    'category': 'UIT_Projects',
    'version': '2.1',

    'depends': ['base', 'website'],

    'js' : ['static/src/js/script.js'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'controllers/opros_template.xml',
        # 'ir.config_parameter.csv'
    ]
}
