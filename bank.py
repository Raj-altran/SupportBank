# ToDo #
# Create export function

from transaction import Transaction
from account import Account
import logging


class Bank():
    name = "bank"
    ledger = {}

    def load(self, csvfile):
        with open(csvfile) as f:
            lines = f.readlines()
        lines.pop(0)

        for line in lines:
            self.add_transaction(line)

    def add_account(self, name):
        self.ledger[name] = Account(name)

    def add_transaction(self, line):
        try:
            TA = Transaction(line)
            AT = Transaction(line).reverse()
        except ValueError:
            logging.info(f'Poor input: {line}')
            return

        name = TA.get_name()
        if name not in self.ledger:
            self.add_account(name)
        self.ledger[name].add_transaction(TA)

        name = AT.get_name()
        if name not in self.ledger:
            self.add_account(name)
        self.ledger[name].add_transaction(AT)

    def print_transactions(self, name):
        self.ledger[name].print_transactions()

    def print_compilation(self):
        for name in self.ledger:
            compiled = self.ledger[name].compile_transactions()
            print(f"---{name}--- Total owed: {self.ledger[name].display_balance()}")
            print("Is owed: \t", end="")
            for item in compiled:
                if compiled[item] > 0:
                    print(f"{item} - {display_money(compiled[item])}, ", end="")
            print(" ")
            print(f"Owes: \t\t", end="")
            for item in compiled:
                if compiled[item] < 0:
                    print(f"{item} - {display_money(compiled[item])}, ", end="")
            print(" ")


    def account_exists(self, name):
        return name in self.ledger


def display_money(value):
    value = abs(value)
    pennies = value % 100
    pounds = value // 100
    if pennies < 10:
        pennies = "0" + str(pennies)
    return f"£{pounds}.{pennies}"
