from ast import With
import unittest

from ..Account import Account
from ..Ops import Withdrawal, Transfer, Deposit
from ..OpLog import Log, OperationLogger

import datetime

class TestOpLogger(unittest.TestCase):
    def test_logger(self):
        account1 = Account("Bobo", "Bobobobobo", "00292445145")
        account2 = Account("BB", "sigma.ug.edu", "00292445145")

        account1.operation(Deposit(500))
        account1.operation(Transfer(account2, 100))

        self.assertEqual(len(account1.op_logger.ops_list), 2)

class TestLogObject(unittest.TestCase):
    def test_log_parse(self):
        current_datetime = datetime.datetime.now()
        operation = Withdrawal(500)

        new_log = Log(current_datetime, operation)

        fmt_string = "[{0}] --- {1} {2}".format(current_datetime, operation.op_name, operation.value)
        log_stringed = "{0}".format(new_log)

        self.assertEqual(log_stringed, fmt_string)



