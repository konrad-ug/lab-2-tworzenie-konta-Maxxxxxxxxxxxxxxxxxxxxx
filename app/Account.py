# from .OpLog import OperationLogger
import uuid

class Account:
    def __init__(self, name, surname, initial_value = 0):
       self.name = name
       self.surname = surname
       self.balance = initial_value
    #    self.log = OperationLogger()
       self.acc_id = uuid.uuid4()

    # def operation(self, op):
    #     op.exec(self)
