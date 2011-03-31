# -*- coding: utf-8 -*-
#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
{
    'name': 'Currency',
    'name_ru_RU': 'Валюта',
    'version': '1.8.0',
    'author': 'B2CK, Dmitry Klimanov',
    'email': 'info@b2ck.com',
    'website': 'http://www.tryton.org/',
    'description': '''Define currencies and exchange rate.
Allow to customize the formatting of the currency amount.
''',
    'description_ru_RU': '''Определение валют и валютных курсов.
    Настройка форматирования суммы валюты.
''',
    'depends': [
        'ir',
        'res',
        'currency',
        'ekd_system',
    ],
    'xml': [
        'xml/currency.xml',
        'xml/currency_rate.xml',
    ],
    'translation': [
        'ru_RU.csv',
    ]
}
