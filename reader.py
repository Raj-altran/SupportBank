import json
import xml.etree.ElementTree as ET
import datetime


class reader():
    lines = []

    def __init__(self):
        self.lines = []

    def load(self, filepath):
        with open(filepath) as f:
            self.lines = f.readlines()
        self.lines.pop(0)


class csvReader(reader):
    lines = []

    def read(self, bank):
        for line in self.lines:
            bank.add_transaction(line)
        return


class jsonReader(reader):
    lines = []

    def load(self, filepath):
        f = open(filepath, 'r')
        self.lines = json.loads(f.read())

    def read(self, bank):
        for item in self.lines:
            line = json_to_line(item)
            bank.add_transaction(line)
        return


class xmlReader(reader):
    lines = []

    def load(self, filepath):
        f = open(filepath, 'r')
        self.lines = f.read()

    def read(self, bank):
        root = ET.fromstring(self.lines)
        for item in root:
            line = xml_to_line(item)
            bank.add_transaction(line)
        return


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
