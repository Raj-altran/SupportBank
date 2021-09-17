# ToDo #
# export a bank

from bank import Bank
import logging

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)
logging.info('SupportBank log start!')


support_bank = Bank("Support Bank")

# Menu
live = True

while live:
    user_input = input("Enter function: ")
    func = user_input.split(" ")[0].lower()
    parameter = user_input[len(func)+1:].lower()
    if func == "list":
        if parameter == "all":
            support_bank.print_compilation()
        elif support_bank.account_exists(parameter):
            support_bank.print_transactions(parameter)
        else:
            print("That name is not in the database.")
    elif func == "import":
        support_bank.load(parameter)
    elif func == "export":
        if parameter == "all":
            support_bank.export_compilation()
        elif support_bank.account_exists(parameter):
            support_bank.export_transactions(parameter)
        else:
            print("That name is not in the database.")
    elif user_input == "exit":
        live = False
    else:
        print("I don't understand, please try again.")








