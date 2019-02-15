import datetime
import time

SLEEP = 0.01


class WithdrawalExceededBalance(Exception):
    def __init__(self, message):
        self.message = message


class MoneyNegative(Exception):
    def __init__(self, message):
        self.message = message


class Money(object):
    def __init__(self, value):
        if value < 0:
            raise MoneyNegative("Money value cannot be negative!")
        self.value = round(value, 2)


class Account(object):
    def __init__(self, balance=0):
        self.records = []
        self.balance = Money(0)
        if balance != 0:
            self.deposit(Money(balance))

    def get_balance(self):
        return self.balance.value

    def add_record(self, credit, debit, balance):
        trans_time = datetime.datetime.now()
        self.records.append([trans_time, credit, debit, balance])

    def deposit(self, amount):
        self.balance.value += amount.value
        self.add_record(debit="", credit=amount.value, balance=self.balance.value)
        time.sleep(SLEEP)
        return "Deposit done."

    def withdraw(self, amount):
        if amount.value > self.balance.value:
            raise WithdrawalExceededBalance("Withdrawal exceeds balance!")
        self.balance.value -= amount.value
        self.add_record(debit=amount.value, credit="", balance=self.balance.value)
        time.sleep(SLEEP)
        return "Withdrawal completed."

    def transfer(self, target_account, amount):
        self.withdraw(amount)
        target_account.deposit(amount)
        return "Transfer done."


class Statements(object):
    def __init__(self, account, filters):
        self.account = account
        self.filters = filters

    def get_statement(self):
        records = self.account.records
        hist_records = "date  ||  credit  ||  debit  ||  balance \n"
        records = [rec for rec in records if (rec[1]*self.filters["credit"] or
                   rec[2] * self.filters["debit"])
                   and (rec[0] >= self.filters["from"] and rec[0] < self.filters["to"])]
        for record in reversed(records):
            hist_records = hist_records + "{} || {} || {} || {}\n".format(record[0], record[1], record[2], record[3])
        return hist_records


class PrintStatements(Statements):
    def __init__(self, account, filters):
        super(PrintStatements, self).__init__(account, filters)

    def print_statements(self):
        print self.get_statement()
        return self.get_statement()
