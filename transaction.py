# ToDo #
# create transaction fields
# create return data function

import datetime


class Transaction():
    date = datetime.datetime(1900, 1, 1)
    sender = ""
    receiver = ""
    amount = 0
    reason = ""

    def __init__(self, input):
        # input example: '01/01/2014,Jon A,Sarah T,Pokemon Training,7.8\n'
        data = input.split(',')
        dateraw = data[0].split("/")
        day = int(dateraw[0])
        month = int(dateraw[1])
        year = int(dateraw[2])

        self.date = datetime.datetime(year, month, day)
        self.sender = data[1]
        self.receiver = data[2]
        self.reason = data[3]

        value = data[4].replace("\n", "")
        value = int(float(value) * 100)
        self.amount = value

    def print_transaction(self):
        if self.amount > 0:
            print(
                f"+++ {self.sender} sent {self.amount} to {self.receiver}. Date: {self.date.strftime('%d-%m-%Y')}."
                f" Reason: {self.reason}")
        else:
            print(
                f"--- {self.sender} was sent {-1*self.amount} from {self.receiver}. Date: {self.date.strftime('%d-%m-%Y')}."
                f" Reason: {self.reason}")

    def get_name(self):
        return self.sender

    def get_name_other(self):
        return self.receiver

    def get_amount(self):
        return self.amount

    def reverse(self):
        self.sender, self.receiver = self.receiver, self.sender
        self.amount *= -1

        return self