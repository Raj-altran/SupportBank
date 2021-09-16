# ToDo #
import logging


class Account():
    name = ""
    balance = 0
    transactions = []

    def __init__(self, name):
        self.name = name
        self.transactions = []
        self.balance = 0

    def display_balance(self):
        sign = ""
        if self.balance < 0:
            sign = "-"

        value = abs(self.balance)
        pennies = value % 100
        pounds = value // 100

        if pennies < 10:
            pennies = "0" + str(pennies)
        return f"{sign}£{pounds}.{pennies}"

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.balance += transaction.get_amount()

    def print_transactions(self):
        running = 0
        for ta in self.transactions:
            ta.print_transaction()
            # running += ta.get_amount()
            # print (running)

        print(f"{self.name} has a balance of: {self.display_balance()}")

    def compile_transactions(self):
        results = {}
        for TA in self.transactions:
            name = TA.get_name_other()
            if name not in results:
                results[name] = 0
            results[name] += TA.get_amount()

        return results
