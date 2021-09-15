# ToDo #
# Create export function

from transaction import Transaction
from account import Account


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
        TA = Transaction(line)
        AT = Transaction(line).reverse()

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

    def account_exists(self, name):
        return name in self.ledger
