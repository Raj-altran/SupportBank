# ToDo #
# Create export function

from transaction import Transaction
from account import Account
import logging
import datetime
from reader import *


class Bank():
    name = "bank"
    ledger = {}

    def __init__(self, name):
        self.name = name
        self.ledger = {}

    def load(self, path):
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

        reader = ""

        if extension == "csv":
            reader = csvReader()
        elif extension == "json":
            reader = jsonReader()
        elif extension == "xml":
            reader = xmlReader()
        else:
            print("File extension not supported.")

        reader.load(path)
        reader.read(self)

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
        return name in self.ledger


def display_money(value):
    value = abs(value)
    pennies = value % 100
    pounds = value // 100
    if pennies < 10:
        pennies = "0" + str(pennies)
    return f"£{pounds}.{pennies}"
