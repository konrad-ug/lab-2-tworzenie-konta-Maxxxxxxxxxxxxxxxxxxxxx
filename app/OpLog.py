import datetime

class OperationLogger:
    def __init__(self):
        self.ops_list = []

    def log_operation(self, op):
        time = datetime.datetime.now()
        new_log = Log(time, op)
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
        if self.op.op_name is not "Transfer":
            return "[{0}] --- {1} {2}".format(self.datetime, self.op.op_name, self.op.value)
        else:
            return "[{0}] --- Transfer {1} to Account#{2}".format(self.datetime, self.op.value, self.op.recipient.acc_id)

