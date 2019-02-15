import pytest
import mock
import datetime

from bank_kata import Account
from bank_kata import Money
from bank_kata import MoneyNegative
from bank_kata import PrintStatements
from bank_kata import WithdrawalExceededBalance


def test_get_init_balance():
    account = Account()
    money = Money(0)
    assert isinstance(account.balance, Money)
    assert account.balance.value == money.value


def test_get_balance():
    account = Account(100)
    assert account.get_balance() == 100


def test_create_account_with_init_balance():
    account = Account(100)
    assert account.balance.value == 100


def test_make_deposit_and_check_balance():
    account = Account()
    money = Money(150)
    assert account.deposit(money) == "Deposit done."
    assert account.balance.value == 150


def test_negative_money():
    with pytest.raises(MoneyNegative):
        Money(-10)


def test_withdraw_and_balance():
    account = Account(100)
    money = Money(80)
    assert account.withdraw(money) == "Withdrawal completed."
    assert account.balance.value == Money(20).value


def test_withdraw_too_much():
    account = Account(100)
    money = Money(120)
    with pytest.raises(WithdrawalExceededBalance):
        account.withdraw(money)
    try:
        account.withdraw(money)
    except WithdrawalExceededBalance:
        assert account.balance.value == 100


def test_transfer():
    account1 = Account(100)
    account2 = Account()
    money = Money(40)
    account1.transfer(account2, money)
    assert account1.balance.value == 60
    assert account2.balance.value == 40


def test_transfer_exceeds():
    account1 = Account(100)
    account2 = Account()
    money = Money(140)
    with pytest.raises(WithdrawalExceededBalance):
        account1.transfer(account2, money)
    try:
        account1.transfer(account2, money)
    except WithdrawalExceededBalance:
        assert account1.balance.value == 100
        assert account2.balance.value == 0


def test_add_single_history_record():
    account = Account(100)
    assert len(account.records) == 1
    account.withdraw(Money(20))
    assert len(account.records) == 2


@mock.patch('bank_kata.datetime')
def test_print_statement(mocked_datetime):
    account = Account()
    mocked_datetime.datetime.now.return_value = datetime.datetime(2019, 2, 5, 12, 32)
    account.deposit(Money(1000))
    mocked_datetime.datetime.now.return_value = datetime.datetime(2019, 2, 6, 12, 32)
    account.deposit(Money(2000))
    mocked_datetime.datetime.now.return_value = datetime.datetime(2019, 2, 7, 12, 32)
    account.withdraw(Money(500))

    expected = """date  ||  credit  ||  debit  ||  balance 
2019-02-07 12:32:00 ||  || 500 || 2500
2019-02-06 12:32:00 || 2000 ||  || 3000
2019-02-05 12:32:00 || 1000 ||  || 1000"""

    st = PrintStatements(account, [])
    st.print_statements()
    # assert st.print_statements() == expected


@mock.patch('bank_kata.datetime')
def test_print_statement(mocked_datetime):
    account = Account()
    mocked_datetime.datetime.now.return_value = datetime.datetime(2019, 2, 5, 12, 32)
    account.deposit(Money(1000.1234))
    mocked_datetime.datetime.now.return_value = datetime.datetime(2019, 2, 6, 12, 32)
    account.deposit(Money(2000))
    mocked_datetime.datetime.now.return_value = datetime.datetime(2019, 2, 7, 12, 32)
    account.withdraw(Money(500))

    from_time = datetime.datetime(2019, 2, 2)
    till_time = datetime.datetime(2019, 2, 9)

    st = PrintStatements(account, filters={"from": from_time, "to": till_time,
                                           "credit": 1, "debit": 1})
    st.print_statements()
