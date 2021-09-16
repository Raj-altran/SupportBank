# ToDo #
# export a bank

from bank import Bank
import logging

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)
logging.info('SupportBank log start!')


support_bank = Bank()

support_bank.load("DodgyTransactions2015.csv")

# Menu
live = True

while live:
    user_input = input("Enter function: ")
    func = user_input.split(" ")[0]
    parameter = user_input[len(func)+1:]
    if func == "List":
        if parameter == "All":
            support_bank.print_compilation()
        elif support_bank.account_exists(parameter):
            support_bank.print_transactions(parameter)
        else:
            print("That name is not in the database.")
    elif user_input == "exit":
        live = False
    else:
        print("I don't understand, please try again.")








