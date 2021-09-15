# ToDo #


class Account():
    name = ""
    balance = 0
    transactions = []

    def __init__(self, name):
        self.name = name
        self.transactions = []
        self.balance = 0

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.balance += transaction.get_amount()

    def print_transactions(self):
        for ta in self.transactions:
            ta.print_transaction()

        print(f"{self.name} has a balance of: {self.balance}")

    def compile_transactions(self):
        results = {}
        for TA in self.transactions:
            name = TA.get_name_other()
            if name not in results:
                results[name] = 0
            results[name] += TA.get_amount()

        return results
