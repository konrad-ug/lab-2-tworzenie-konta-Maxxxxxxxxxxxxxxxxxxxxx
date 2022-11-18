import datetime
import re
import uuid

class AbstractAccount:
    def __init__(self):
        pass
    
    def operation(self, op):
        if not isinstance(op, Deposit) or isinstance(op, Credit):
            if op.value > self.balance:
                return False
            else:
                if not isinstance(op, Transfer):
                    self.op_logger.log_operation(op)
                    return op.exec(self)
                elif isinstance(op, Transfer):
                    self.op_logger.log_operation(op)
                    op.recipient.op_logger.log_received_transfer(op.value, self.acc_id, op.is_express)
                    return op.exec(self)
        else:
            self.op_logger.log_operation(op)
            return op.exec(self)

    def zaciagnij_kredyt(self, value):
        return self.operation(Credit(value))

class Account(AbstractAccount):
    def __init__(
        self, name, surname, 
        pesel, initial_value = 0, 
        prom = None):

        self.name = name
        self.surname = surname
        self.pesel = self._validate_pesel(pesel)
        self.balance = self._validate_promo(prom, initial_value)
        self.op_logger = OperationLogger()
        self.acc_id = uuid.uuid4()
        self.historia = []

    def _validate_promo(self, code, initial):
        if code == None:
            return initial

        fmt_digits = ""+self.pesel[0]+self.pesel[1]+self.pesel[2]+self.pesel[3]
        promo_match = re.search("^(PROM_).{3}$", code)
        digits_match = re.search("^[0-6][0-9](0[0-9]|1[0-2])$", fmt_digits)

        if promo_match and digits_match:
            return initial+50 
        else:
            return initial

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

class AccountFirma(AbstractAccount):
    def __init__(self, name, nip, initial_value = 0):
        self.company_name = name
        self.nip = nip
        self.balance = initial_value
        self.op_logger = OperationLogger()
        self.acc_id = uuid.uuid4()
        self.historia = []

# --------------------------------- Operacje ---------------------------------

class Withdrawal:
    def __init__(self, value):
        self.value = value
        self.op_name = "Withdrawal"

    def exec(self, account):
        account.balance = account.balance - self.value
        account.historia.append(-self.value)
        return True


class Credit:
    def __init__(self, value):
        self.value = value
        self.op_name = "Credit"

    def check_eligible_enterprise(self, account) -> bool:
        if account.balance > self.value*2 and -1775 in account.historia:
            return True
        else:
            return False

    def check_eligible_normal_acc(self, account):
        if len(account.historia) >= 3:
            state = True
            if account.historia[-1] <= 0:
                state = False
            if account.historia[-2] <= 0:
                state = False
            if account.historia[-3] <= 0:
                state = False

            if state:
                return True
            elif not state:
                if len(account.historia) > 5:
                    sum = 0
                    for i in range(1,6):
                        sum += account.historia[-i]
                    if sum > self.value:
                        return True
                    else:
                        return False
        else:
            return False

    def exec(self, account):
        if type(account) == Account:
            is_eligible = self.check_eligible_normal_acc(account)
        elif type(account) == AccountFirma:
            is_eligible = self.check_eligible_enterprise(account)

        if is_eligible:
            account.balance += self.value
            account.historia.append(self.value)
        return is_eligible

class Transfer:
    def __init__(self, recipient, value, is_express = False):
        self.recipient = recipient
        self.value = value
        self.op_name = "Transfer"
        self.is_express = is_express

    def exec(self, account):
        if self.is_express:
            switch = { AccountFirma: 5, Account: 1 }
            account.balance -= switch[type(account)]
            account.historia.append(-switch[type(account)])

        account.balance = account.balance - self.value
        account.historia.append(-self.value)
        self.recipient.balance = self.recipient.balance + self.value
        self.recipient.historia.append(self.value)
        return True


class Deposit:
    def __init__(self, value):
        self.value = value
        self.op_name = "Deposit"

    def exec(self, account):
        account.balance = account.balance + self.value
        account.historia.append(self.value)
        return True

class OperationLogger:
    def __init__(self):
        self.ops_list = []

    def log_operation(self, op):
        time = datetime.datetime.now()
        new_log = Log(time, op)
        self.ops_list.append(new_log)

        return new_log

    def log_received_transfer(self, value, sender_id, is_express):
        time = datetime.datetime.now()
        new_log = ReceivedTransferLog(time, value, sender_id)
        self.ops_list.append(new_log)

        return new_log

    def show(self):
        for log in self.ops_list:
            print(log)

class Log:
    def __init__(self, datetime, op):
        self.datetime = datetime
        self.op = op

    def __repr__(self):
        if not isinstance(self.op, Transfer):
            return "[{0}] --- {1} {2}".format(self.datetime, self.op.op_name, self.op.value)
        else:
            return "[{0}] --- Transfer {1} to Account#{2}".format(self.datetime, self.op.value, self.op.recipient.acc_id)


class ReceivedTransferLog(Log):
    def __init__(self, datetime, value, sender_id):
        self.datetime = datetime
        self.value = value
        self.sender_id = sender_id

    def __repr__(self):
        return "[{0}] --- Transfer {1} from Account#{2}".format(self.datetime, self.value, self.sender_id)