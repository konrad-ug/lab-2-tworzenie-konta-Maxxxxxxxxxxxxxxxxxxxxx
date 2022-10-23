import unittest

from ..Account import Account
from ..Ops import Withdrawal, Transfer

class TestCreateBankAccount(unittest.TestCase):
    def test_create_acc(self):
        acc1 = Account("Dariusz", "Januszewski")
        self.assertEqual(acc1.name, "Dariusz", "Imie nie zostało zapisane!")
        self.assertEqual(acc1.surname, "Januszewski", "Nazwisko nie zostało zapisane!")
        self.assertEqual(acc1.balance, 0, "Saldo nie jest zerowe!")

    #tutaj proszę dodawać nowe testy

# class TestOperations(unittest.TestCase):
#     def test_withdraw(self):
#         account = Account("wp", "ug", 1000)
#         account.operation(Withdrawal(500))
#         self.assertEqual(account.balance, 500, "Saldo nie zgadza się z wartością wyciągu")

#     def test_transfer(self):
#         sender = Account("sender", "senderowski", 1500)
#         recipient = Account("recipient", "recipientowski")
#         sender.operation(Transfer(recipient, 500))
#         self.assertEqual(recipient)

# class TestPESEL(unittest.TestCase):
#     def test_pesel_chars(self):
#         pass