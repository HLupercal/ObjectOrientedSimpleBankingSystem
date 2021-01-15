import sys


class BankingSystem:

    def __init__(self):
        self.accounts = {}
        self.current_account = None  # create a null object

    def create_account(self):
        acc = Account()
        self.accounts += {acc.card_number, acc}
        return MainMenu(self)

    def handle_login(self):
        card_number = input("Enter your card number:")
        card_pin = input("Enter your PIN:")
        self._try_login(card_number, card_pin)

    def check_current_account_balance(self):
        print(self.current_account.balance)
        return AccountMenu(self)

    def _try_login(self, card_number, pin):
        if self.accounts[card_number]:
            self._login(card_number, pin)

    def _login(self, card_number, pin):
        if self.accounts[card_number].pin == pin:
            print("You have successfully logged in!")
            self.current_account = self.accounts[card_number]
            return AccountMenu(self)
        else:
            print("Wrong card number or PIN!")
            return MainMenu(self)

    def handle_logout(self):
        self.current_account = None # create null object
        return MainMenu(self)


class Account:

    def __init__(self):
        self.card_number = "123"
        self.pin = "1111"
        self.balance = 0


class ExitMenu:
    def __init__(self, bs: BankingSystem):
        self.bs = bs

    def wait_for_input(self):
        print("Bye!")
        sys.exit()


class MainMenu:
    option1 = "1. Create an account"
    option2 = "2. Log into account"
    option0 = "0. Exit"

    def __init__(self, bs: BankingSystem):
        self.bs = bs

    def wait_for_input(self):
        self.print_menu()
        selected_option = int(input())
        if selected_option == 1:
            return self.handle1()
        elif selected_option == 2:
            return self.handle2()
        elif selected_option == 0:
            return self.handle0()

    def print_menu(self):
        print(self.option1)
        print(self.option2)
        print(self.option0)

    def handle1(self):
        return self.bs.create_account()

    def handle2(self):
        return self.bs.handle_login()

    def handle0(self):
        val = ExitMenu(self.bs)
        return val


class AccountMenu:
    option1 = "1. Balance"
    option2 = "2. Log out"
    option0 = "0. Exit"

    def __init__(self, bs: BankingSystem):
        self.bs = bs

    def print_menu(self):
        print(self.option1)
        print(self.option2)
        print(self.option0)

    def wait_for_input(self):
        self.print_menu()
        selected_option = int(input())
        if selected_option == 1:
            return self.handle1()
        elif selected_option == 2:
            return self.handle2()
        elif selected_option == 0:
            return self.handle0()

    def handle1(self):
        return self.bs.check_current_account_balance()

    def handle2(self):
        return self.bs.handle_logout()

    def handle0(self):
        return self.bs.handle_login()


def run():
    banking_system = BankingSystem()
    menu = MainMenu(bs=banking_system)
    while True:
        menu = menu.wait_for_input()


run()
