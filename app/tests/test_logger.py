from ast import With
import unittest

from ..Account import Account
from ..Account import Withdrawal, Transfer, Deposit
from ..Account import Log, OperationLogger

import datetime

valid_pesel = "02252928673"

class TestOpLogger(unittest.TestCase):
    def test_logger(self):
        account1 = Account("Bobo", "Bobobobobo", "00292445145")
        account2 = Account("BB", "sigma.ug.edu", "00292445145")

        account1.operation(Deposit(500))
        account1.operation(Transfer(account2, 100))

        self.assertEqual(len(account1.op_logger.ops_list), 2)

    # def test_log_transfer(self):
    #     a1 = Account("Zenek", "Gdula", "00292445145", 500)
    #     recipient = Account("Greta", "Gdula", "00292445145")

    #     a1.operation(Transfer(recipient, 500))

    #     a1.op_logger.show()
    #     recipient.op_logger.show()

    def test_transfer_receive(self):
        sender = Account("haha", "asdads", valid_pesel, 1500)
        recipient = Account("Zenon", "Gdula", valid_pesel)

        sender.operation(Transfer(recipient, 500))
        length = len(recipient.op_logger.ops_list)

        self.assertEqual(length, 1)

class TestLogObject(unittest.TestCase):
    def test_log_parse(self):
        current_datetime = datetime.datetime.now()
        operation = Withdrawal(500)

        new_log = Log(current_datetime, operation)

        fmt_string = "[{0}] --- {1} {2}".format(current_datetime, operation.op_name, operation.value)
        log_stringed = "{0}".format(new_log)

        self.assertEqual(log_stringed, fmt_string)



