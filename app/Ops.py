class Operation:
    def exec(self, account):
        pass

class Withdrawal(Operation):
    def __init__(self, value):
        self.value = value
        self.op_name = "Withdrawal"

    def exec(self, account):
        account.balance = account.balance - self.value

class Transfer(Operation):
    def __init__(self, recipient, value):
        self.recipient = recipient
        self.value = value
        self.op_name = "Transfer"

    def exec(self, account):
        account.balance = account.balance - self.value
        self.recipient.balance = self.recipient.balance + self.value

class Deposit(Operation):
    def __init__(self, value):
        self.value = value
        self.op_name = "Deposit"

    def exec(self, account):
        account.balance = account.balance + self.value

    