from datetime import date
from decimal import Decimal
import re


class AnotherActiveSessionException(Exception):
    def __init__(self, message, errors=None, request=None):
        super(AnotherActiveSessionException, self).__init__(message)

        self.errors = errors
        print('[D] Request ({}): {}'.format(request.status_code, request.content.decode()))


class MaintenanceException(Exception):
    def __init__(self, message, errors=None, request=None):
        super(MaintenanceException, self).__init__(message)

        self.errors = errors
        print('[D] Request ({}): {}'.format(request.status_code, request.content.decode()))


class GeneralException(Exception):
    def __init__(self, message, errors=None, request=None):
        super(GeneralException, self).__init__(message)

        self.errors = errors

        print('[D] Request ({}): {}'.format(request.status_code, request.content.decode()))


class Transaction(object):

    def __init__(self, description):
        self.id = 0
        self.value = Decimal(0.00)
        self.sign = '+'
        self.description = description
        self.date = date.today()
        self.currency = '$'

        self.raw = {}

    def get_value(self):
        return '{} {}'.format(self.currency, self.value if self.sign != '-' else self.value * -1)

    def __repr__(self):
        return 'Transaction #{} - {} on {}, value {}'.format(self.id, self.description, self.date, self.get_value())

    def print_info(self):
        print('[{}] {} {}'.format(self.date, self.description, self.get_value()))


class App(object):

    def __init__(self, name):

        self.name = ''
        self.platform = {}
        self.platform['android'] = {'version': 0, 'url': ''}
        self.platform['ios'] = {'version': 0, 'url': ''}
        self.platform['windowsphone'] = {'version': 0, 'url': ''}

        self.eula_url = ''

    def __repr__(self):
        return 'App {}, with versions {} (Android), {} (iOS) and {} (Windows Phone)'.format(self.name, self.platform['android']['version'], self.platform['ios']['version'], self.platform['windowsphone']['version'])

    def print_info(self):
        print('[*] EULA Url: {}'.format(self.eula_url))
        print()
        print('[*] Android Last Version: {}'.format(self.platform['android']['version']))
        print('[*] iOS Last Version: {}'.format(self.platform['ios']['version']))
        print('[*] Windows Phone Last Version: {}'.format(self.platform['windowsphone']['version']))


class Account(object):

    def __init__(self, branch=None, number=None, password=None, document=None, card=None, dac='', account_type='bank', validator=None):
        self.bank = 'Generic'
        self.transactions = []
        self.currency = '$'

        self.overdraft = Decimal(0.00)
        self.interest = Decimal(0.00)
        self.personal_credit = Decimal(0.0)

        self.account_type = account_type
        self.card = card
        self.document = document
        self.company = ''
        self.status = ''
        self.service_name = ''
        self.password = password
        self.branch = branch
        self.number = number
        self.password = password
        self.dac = dac

        self.balance = 0
        self.sign = '+'
        self.segment = ''

        self.type = ''

        self.owner = None

        self.app = App('Generic')

    def get_interest(self):
        return '{} {}'.format(self.currency, self.interest)

    def get_overdraft(self):
        return '{} {}'.format(self.currency, self.overdraft)

    def get_balance(self):
        return '{} {}'.format(self.currency, self.balance if self.sign != '-' else self.balance * -1)

    def __repr__(self):
        if self.account_type == 'bank':
            return 'Bank Account at {}, Branch {}, Number {}, Segment {} {}, with balance of {}'.format(self.bank, self.branch, self.number, self.type, self.segment, self.get_balance())
        elif self.account_type == 'card':
            return 'Card Account at {}, Number {}, Document {}, with balance of {}'.format(self.bank, self.card, self.document, self.get_balance())

    def print_info(self):
        if self.account_type == 'bank':
            print('[*] Account Branch: {}'.format(self.branch))
            print('[*] Account Number: {}{}'.format(self.number, self.dac))
            print('[*] Account Segment: {}'.format(self.segment))
            print('[*] Account Type: {}'.format(self.type))
        elif self.account_type == 'card':
            print('[*] Service Name: {}'.format(self.service_name))
            print('[*] Card Status: {}'.format(self.status))
            print('[*] Company: {}'.format(self.company))
            print('[*] Owner: {}'.format(self.owner.name))
            print('[*] Card Numreter: {}'.format(self.card))
            print('[*] Document: {}'.format(self.document))


class Owner(object):

    def __init__(self, name):
        self.name = name
        self.document = ''
        self.birthday = None

    def __repr__(self):
        if not self.birthday:
            return 'Owner {}, with document {}'.format(self.name, self.document)
        else:
            return 'Owner {}, with document {}, born on {}'.format(self.name, self.document, self.birthday)

    def print_info(self):
        print('[*] Account Owner: {}'.format(self.name))
        print('[*] Account Owner Document: {}'.format(self.document))
        if self.birthday:
            print('[*] Account Owner Birthday: {}'.format(self.birthday.strftime('%Y-%m-%d')))


class BankScraper(object):

    def validate(self):
        if self.validator:
            for f in self.validator.fields:
                if ':' in f:
                    method = f.split(':')[0]
                    field = f.split(':')[1]
                else:
                    method = field = f
                if not self.validator.validate(method, getattr(self.account, field)):
                    print('[!] Invalid field {}'.format(field))
                    exit(1)

    def get_digits(self, value):
        return re.sub(r'[^\d]+', '', value)

    def login(self):
        pass

    def logout(self):
        pass

    def get_transacations(self):
        pass

    def get_balance(self):
        pass

    def pre_login_warmup(self):
        pass

    def post_login_warmup(self):
        pass

    def pre_transactions_warmup(self):
        pass

    def post_transactions_warmup(self):
        pass

    def pre_logout_warmup(self):
        pass

    def post_logout_warmup(self):
        pass
