from .OpLog import OperationLogger

import re
import uuid

class Account:
    def __init__(self, name, surname, pesel, initial_value = 0, prom = None):
       self.name = name
       self.surname = surname
       self.pesel = self._validate_pesel(pesel)
       self.balance = self._validate_promo(prom, initial_value)
       self.op_logger = OperationLogger()
       self.acc_id = uuid.uuid4()

    #    self._validate_promo(prom)

    def operation(self, op):
        op.exec(self)
        self.op_logger.log_operation(op)

    def receive_transfer(self, transfer):
        pass

    def _validate_promo(self, code, initial):
        if code == None:
            return initial

        # promo_regex = re.compile("(PROM_).{3}$")
        # digits_regex = re.compile("[0-6][0-9](0[0-9]|1[0-2])")

        fmt_digits = ""+self.pesel[0]+self.pesel[1]+self.pesel[2]+self.pesel[3]

        promo_match = re.search("^(PROM_).{3}$", code)
        digits_match = re.search("^[0-6][0-9](0[0-9]|1[0-2])$", fmt_digits)

        if promo_match and digits_match:
            return initial+50 
        else:
            return initial

        # if promo_regex.match(code) and digits_regex.match(fmt_digits):
        #     return initial+50
        # else:
        #     return initial

    def _validate_pesel(self, pesel):
        if len(pesel) != 11:
            return "Niepoprawny PESEL!"

        checksum_weights = [1,3,7,9,1,3,7,9,1,3]
        checksum = 0

        for i in range(len(pesel) - 1):
            checksum += int(pesel[i]) * checksum_weights[i]

        comparison_value = None
        if checksum % 10 == 0:
            comparison_value = 0
        else:
            comparison_value = 10 - checksum % 10

        if comparison_value == int(pesel[10]):
            return pesel
        else:
            return "Niepoprawny PESEL!"
            # raise ValueError("Podano nieprawidłowy pesel!")