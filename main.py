class BankingSystem:

    def __init__(self):
        self.accounts = {}

    def old_run(self):
        while True:
            self._print_main_menu()
            option = int(input())
            if option == 1:
                acc = self.create_account()
                print("Your card number:")
                print(acc.card_number)
                print("Your card PIN:")
                print(acc.pin)
            elif option == 2:
                card_number = input("Enter your card number:")
                card_pin = input("Enter your PIN:")
                self.handle_login(card_number, card_pin)
            else:
                break

    def create_account(self):
        acc = Account()
        self.accounts += {acc.card_number, acc}
        return MainMenu()

    def handle_login(self):
        card_number = input("Enter your card number:")
        card_pin = input("Enter your PIN:")
        self._try_login(card_number, card_pin)

    def _try_login(self, card_number, pin):
        if self.accounts[card_number]:
            self._login(card_number, pin)

    def _login(self, card_number, pin):
        if self.accounts[card_number].pin == pin:
            print("You have successfully logged in!")
            return AccountMenu()
        else:
            print("Wrong card number or PIN!")
            return MainMenu()

    def _print_main_menu(self):
        print("""1. Create an account
    2. Log into account
    0. Exit
    """)


class Account:

    def __init__(self):
        self.card_number = "123"
        self.pin = "1111"
        self.balance = 0


class MainMenu:
    option1 = "1. Create an account"
    option2 = "2. Log into account"
    option0 = "0. Exit"

    def __init_(self, bs: BankingSystem):
        self.bs = bs

    def wait_for_input(self):
        self.print_menu()
        selected_option = int(input())
        if selected_option == 1:
            self.handle1()
        elif selected_option == 2:
            self.handle2()
        elif selected_option == 0:
            self.handle0()

    def print_menu(self):
        print(self.option1)
        print(self.option2)
        print(self.option0)

    def handle1(self):
        return self.bs.create_account()

    def handle2(self):
        return self.bs.handle_login()

    def handle0(self):
        return self.bs.handle_login()


class AccountMenu:
    option1 = "1. Balance"
    option2 = "2. Log out"
    option0 = "0. Exit"

    def print_menu(self):
        print(self.option1)
        print(self.option2)
        print(self.option0)


def run():
    banking_system = BankingSystem()
    menu = MainMenu(bs=banking_system)
    while True:
        menu = menu.wait_for_input()


run()
