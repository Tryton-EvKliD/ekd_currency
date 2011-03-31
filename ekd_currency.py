# -*- coding: utf-8 -*-
#This file is part of Tryton.  The COPYRIGHT file at the top level
#of this repository contains the full copyright notices and license terms.
import time
import datetime
from decimal import Decimal, ROUND_HALF_EVEN
from trytond.model import ModelView, ModelSQL, fields
from trytond.tools import safe_eval, datetime_strftime
from trytond.backend import TableHandler, FIELDS
from trytond.transaction import Transaction

class Currency(ModelSQL, ModelView):
    _name = 'currency.currency'
    multy_rates = fields.One2Many('ekd.currency.rate', 'currency', 'Rates')

    def compute(self, from_currency, amount, to_currency, round=True):
        '''
        Take a currency and an amount
        Return the amount to the new currency
        Use the rate of the date of the context or the current date
        '''
        date_obj = self.pool.get('ir.date')
        lang_obj = self.pool.get('ir.lang')
        if amount == Decimal('0.0'):
            return amount
        if isinstance(from_currency, (int, long)):
            from_currency = self.browse(from_currency)
        if isinstance(to_currency, (int, long)):
            to_currency = self.browse(to_currency)
        if to_currency == from_currency:
            if round:
                return self.round(to_currency, amount)
            else:
                return amount
        if (not from_currency.rate) or (not to_currency.rate):
            date = Transaction().context.get('date', date_obj.today())
            if not from_currency.rate:
                name = from_currency.name
            else:
                name = to_currency.name

            for code in [Transaction().language, 'en_US']:
                lang_ids = lang_obj.search([
                    ('code', '=', code),
                    ])
                if lang_ids:
                    break
            lang = lang_obj.browse(lang_ids[0])

            self.raise_user_error('no_rate', (name,
                datetime_strftime(date, str(lang.date))))
        if round:
            return self.round(to_currency,
                    amount / from_currency.unit_from * to_currency.rate)
        else:
            return amount / from_currency.unit_from * to_currency.rate

Currency()

class MultyRate(ModelSQL, ModelView):
    'Multy Rate'
    _name = 'ekd.currency.rate'
    _description = __doc__
    _rec_name = 'date'

    date = fields.Date('Date', required=True, select=1)
    rate = fields.Numeric('Rate', digits=(12, 6), required=1)
    currency = fields.Many2One('currency.currency', 'Currency to',
            ondelete='CASCADE',)
    unit_from = fields.Numeric('Unit Currency', digits=(12, 6), required=1)
    currency_from = fields.Many2One('currency.currency', 'Currency from',
            ondelete='CASCADE',)
    code = fields.Function(fields.Char('Code Currency', size=3), 'get_code')
    code_from = fields.Function(fields.Char('Code Currency From', size=3), 'get_code')
    type_rate = fields.Selection([
            ('main','Main'),
            ('other','Other')
            ], 'Type Rate')

    def __init__(self):
        super(MultyRate, self).__init__()
        self._sql_constraints = [
            ('date_currency_currency_from_uniq', 'UNIQUE(date, currency, currency_from, type_rate)',
                'A currency can only have one rate by date!'),
        ]
        self._order.insert(0, ('date', 'DESC'))
        self._order.insert(1, ('currency_from', 'DESC'))

    def init(self, module_name):
        super(MultyRate, self).init(module_name)

    def check_xml_record(self, ids, values):
        return True

    def default_unit_from(self):
        return Decimal('1.0')

    def default_type_rate(self):
        return 'main'

    def get_code(self, ids, names):
        '''
        Return the code currency
        '''
        res = {}
        for currency_rate in self.browse(ids):
            for name in names:
                if name == 'code':
                    res[name][currency_rate.id] = currency_rate.currency.code
                if name == 'code_from':
                    res[name][currency_rate.id] = currency_rate.currency_from.code
        raise Exception(str(names), str(res))
        return res

MultyRate()
