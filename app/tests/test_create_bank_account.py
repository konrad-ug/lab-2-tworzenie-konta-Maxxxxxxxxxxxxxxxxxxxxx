import unittest
import re

from ..Account import Account, AccountFirma
from ..Account import Withdrawal, Transfer, Deposit

valid_pesel = "02252928673"

class TestCreateBankAccount(unittest.TestCase):
    def test_create_acc(self):
        acc1 = Account("Dariusz", "Januszewski", "02252928673")
        self.assertEqual(acc1.name, "Dariusz", "Imie nie zostało zapisane!")
        self.assertEqual(acc1.surname, "Januszewski", "Nazwisko nie zostało zapisane!")
        self.assertEqual(acc1.balance, 0, "Saldo nie jest zerowe!")

    def test_promocode_passed(self):
        promocode = "PROM_423"
        account = Account("Zenio", "Gdula", "53012007439", 0, promocode)

        self.assertRegex(promocode, "^(PROM_).{3}$")
        self.assertEqual(account.balance, 50)

    def test_promocode_failed(self):
        promocode = "PROM_2137"
        account = Account("Karol", "Wojtyła", "33260519847", 0, promocode)

        self.assertNotRegex(promocode, "^(PROM_).{3}$")
        self.assertEqual(account.balance, 0)

    #tutaj proszę dodawać nowe testy

class TestOperations(unittest.TestCase):
    def test_withdraw(self):
        account = Account("wp", "ug", "02252928673", 1000)
        account.operation(Withdrawal(500))
        self.assertEqual(account.balance, 500, "Saldo nie zgadza się z wartością wyciągu")

    def test_transfer(self):
        sender = Account("sender", "senderowski", "02252928673", 1500)
        recipient = Account("recipient", "recipientowski", "02252928673")
        sender.operation(Transfer(recipient, 500))
        self.assertEqual(recipient.balance, 500, "Konto adresata nie zgadza się!")
        self.assertEqual(sender.balance, 1000, "Konto nadawcy nie zgadza się!")

    def test_deposit(self):
        account = Account("Imie", "Nazwisko", "02252928673")
        account.operation(Deposit(1200))
        self.assertEqual(account.balance, 1200, "Stan konta nie zgadza się!")

    def test_transfer_express_regular(self):
        sender = Account("Zenon", "Gdula", valid_pesel, 100)
        recipient = Account("Max", "Schlamberger", valid_pesel)

        sender.operation(Transfer(recipient, 90, True))
        self.assertEqual(sender.balance, 9)

    def test_transfer_express_firma(self):
        sender = AccountFirma("JP Firma", "4202137000", 2137)
        recipient = AccountFirma("Polska Policja", "99700011143")

        sender.operation(Transfer(recipient, 137, True))
        self.assertEqual(sender.balance, 1995)

class TestPESEL(unittest.TestCase):
    def test_pesel_chars(self):
        account = Account("Zenon", "Gdula", "02252928673")
        self.assertRegex(account.pesel, "^[0-9]{11}$")

    # Chciałem zrobić walidacje po exception, ale polecenie oczekuje czegoś prostszego 

    # def test_pesel_not_valid(self):
    #     self.assertRaises(ValueError, Account, "Zenon", "Gdula", "94319932138")

    def test_pesel_valid(self):
        acc = Account("Zenon", "Gdula", "02252928673");

        checksum_weights = [1,3,7,9,1,3,7,9,1,3]
        checksum = 0

        for i in range(len(acc.pesel) - 1):
            checksum += int(acc.pesel[i]) * checksum_weights[i]

        comparison_value = None
        if checksum % 10 == 0:
            comparison_value = 0
        else:
            comparison_value = 10 - checksum % 10
        
        self.assertEqual(int(acc.pesel[10]), comparison_value)

class TestCreateAccountFirma(unittest.TestCase):
    def success_create_firma_account_nip(self):
        firma = AccountFirma("Usługi Informatyczne Wiesław Pawłowski", "4202137000")

        self.assertEqual(firma.nip, "4202137000")

    def fail_create_firma_account_nip(self):
        firma = AccountFirma("Antmicro", "100643223918")

        self.assertEqual(firma.nip, "Niepoprawny NIP!")