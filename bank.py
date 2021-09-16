# ToDo #
# Create export function

from transaction import Transaction
from account import Account
import logging
import json
import xml.etree.ElementTree as ET
import datetime


class Bank():
    name = "bank"
    ledger = {}

    def __init__(self, name):
        self.name = name
        self.ledger = {}

    def load(self, path):
        extension = path.split(".")[1]
        if extension == "csv":
            with open(path) as f:
                lines = f.readlines()
            lines.pop(0)

            for line in lines:
                self.add_transaction(line)
        elif extension == "json":
            f = open(path, 'r')
            data = json.loads(f.read())
            for item in data:
                line = json_to_line(item)
                self.add_transaction(line)
        elif extension == "xml":
            f = open(path, 'r')
            data = f.read()
            root = ET.fromstring(data)
            for item in root:
                line = xml_to_line(item)
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
        filename = f"{self.name} - All.csv"
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


def json_to_line(json):
    # json example {'date': '2013-12-17', 'fromAccount': 'Sarah T', 'toAccount': 'Ben B', 'narrative': 'Pokemon Training', 'amount': 8.72}
    # line example: '01/01/2014,Jon A,Sarah T,Pokemon Training,7.8'
    date = json['date'].split("-")
    date.reverse()
    date = "/".join(date)
    sender = json['fromAccount']
    receiver = json['toAccount']
    reason = json['narrative']
    amount = json['amount']

    line = f"{date},{sender},{receiver},{reason},{amount}"
    return line


def xml_to_line(xml):
    # line example: '01/01/2014,Jon A,Sarah T,Pokemon Training,7.8'
    date = xml.attrib
    date = datetime.datetime(1900, 1, 1) + datetime.timedelta(days=int(date['Date']) - 1)
    date = date.strftime('%d/%m/%Y')
    sender = xml[2][0].text
    receiver = xml[2][1].text
    reason = xml[0].text
    amount = xml[1].text

    line = f"{date},{sender},{receiver},{reason},{amount}"
    return line
