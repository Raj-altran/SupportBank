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
        self.sender = data[1].lower()
        self.receiver = data[2].lower()
        self.reason = data[3].lower()

        value = data[4].replace("\n", "")
        value = int(float(value) * 100)
        self.amount = value

    def display_amount(self):
        value = abs(self.amount)
        pennies = value % 100
        pounds = value // 100
        if pennies < 10:
            pennies = "0"+str(pennies)
        return f"£{pounds}.{pennies}"

    def display_date(self):
        return self.date.strftime('%d-%m-%Y')

    def print_transaction(self):
        if self.amount > 0:
            print(
                f"+++ {self.sender} sent {self.display_amount()} to {self.receiver}. "
                f"Date: {self.display_date()}. Reason: {self.reason}")
        else:
            print(
                f"--- {self.sender} was sent {self.display_amount()} from {self.receiver}."
                f" Date: {self.display_date()}. Reason: {self.reason}")

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

    def export_format(self):
        # line example: '01/01/2014,Jon A,Sarah T,Pokemon Training,7.8'
        sign = ""
        if self.amount < 0:
            sign = "-"
        pounds = abs(self.amount)//100
        pence = abs(self.amount)%100
        amount = f"{sign}{pounds}.{pence}"
        line = f"{self.date.strftime('%d/%m/%Y')},{self.sender},{self.receiver},{self.reason},{amount}\n"
        return line
