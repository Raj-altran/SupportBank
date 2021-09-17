# ToDo #
# Create export function

from transaction import Transaction
from account import Account
import logging
import datetime
from reader import *


class Bank():
    __name = "bank"
    __ledger = {}

    def __init__(self, name):
        self.name = name
        self.ledger = {}

    def load(self, path):
        path = path.lower()
        try:
            f = open(path)
        except IOError:
            print("File not found.")
            return
        extension = ""
        try:
            extension = path.split(".")[1]
        except IndexError:
            print("File must have an extention")
            return

        file_reader = ""

        if extension == "csv":
            file_reader = csvReader()
        elif extension == "json":
            file_reader = jsonReader()
        elif extension == "xml":
            file_reader = xmlReader()
        else:
            print("File extension not supported.")
            return

        file_reader.load(path)
        file_reader.read(self)
        print("Import successful.")

    def add_account(self, name):
        self.ledger[name] = Account(name)

    def add_transaction(self, line):
        try:
            transaction = Transaction(line)
            reverse_transaction = Transaction(line).reverse()
        except ValueError:
            logging.warning(f'Poor input: {line}')
            return

        name = transaction.get_name()
        if name not in self.ledger:
            self.add_account(name)
        self.ledger[name].add_transaction(transaction)

        name = reverse_transaction.get_name()
        if name not in self.ledger:
            self.add_account(name)
        self.ledger[name].add_transaction(reverse_transaction)

    def print_transactions(self, name):
        self.ledger[name].print_transactions()

    def export_transactions(self, name):
        self.ledger[name].export_transactions(self.name)

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

    def export_compilation(self):
        filename = f"{self.name} - All.txt"
        f = open(filename, 'w')
        lines = []

        for name in self.ledger:
            compiled = self.ledger[name].compile_transactions()
            lines.append(f"---{name}--- Total owed: {self.ledger[name].display_balance()}\n")
            lines.append("Is owed: \t")
            for item in compiled:
                if compiled[item] > 0:
                    lines.append(f"{item} - {display_money(compiled[item])}, ")
            lines.append("\n")
            lines.append(f"Owes: \t\t")
            for item in compiled:
                if compiled[item] < 0:
                    lines.append(f"{item} - {display_money(compiled[item])}, ")
            lines.append("\n")

        f.writelines(lines)
        print(f"{filename} created.")

    def account_exists(self, name):
        for item in self.ledger:
            if name == item.lower():
                return True
        return False


def display_money(value):
    value = abs(value)
    pennies = value % 100
    pounds = value // 100
    if pennies < 10:
        pennies = "0" + str(pennies)
    return f"£{pounds}.{pennies}"
