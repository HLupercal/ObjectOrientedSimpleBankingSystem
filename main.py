import sys


class BankingSystem:

    def __init__(self):
        self.accounts = {}
        self.current_account = None  # create a null object

    def create_account(self):
        acc = Account()
        self.accounts[acc.card_number] = acc
        acc.print_account_credentials()
        return MainMenu(self)

    def handle_login(self):
        card_number = input("Enter your card number:")
        card_pin = input("Enter your PIN:")
        return self._try_login(card_number, card_pin)

    def check_current_account_balance(self):
        print(self.current_account.balance)
        return AccountMenu(self)

    def handle_logout(self):
        self.current_account = None  # create null object
        return MainMenu(self)

    def _try_login(self, card_number, pin):
        if self._are_credentials_valid(card_number, pin):
            print("You have successfully logged in!")
            self.current_account = self.accounts[card_number]
            return AccountMenu(self)
        else:
            print("Wrong card number or PIN!")
            return MainMenu(self)

    def _are_credentials_valid(self, card_number, pin):
        return card_number in self.accounts and self.accounts[card_number].pin == pin




class Account:

    def __init__(self):
        self.card_number = "123"
        self.pin = "1111"
        self.balance = 0

    def print_account_credentials(self):
        print("Your card has been created")
        print("Your card number:")
        print(self.card_number)
        print("Your card PIN:")
        print(self.pin)


class MenuItem:

    def __init__(self, message, handler_function):
        self.message = message
        self.handler_function = handler_function

    def invoke(self):
        return self.handler_function()


class GenericMenu:
    def __init__(self, bs: BankingSystem):
        self.bs = bs

    def wait_for_input(self):
        """
        empty interface
        """
        pass


class ExitMenu(GenericMenu):
    def __init__(self, bs: BankingSystem):
        super().__init__(bs)

    def wait_for_input(self):
        print("Bye!")
        sys.exit()


class MainMenu(GenericMenu):

    def __init__(self, bs: BankingSystem):
        super().__init__(bs)
        self.options_dict = {1: MenuItem("Create an account", self._handle_account_creation),
                             2: MenuItem("Log into account", self._handle_login),
                             0: MenuItem("Exit", self._handle_exit)}

    def wait_for_input(self):
        self.print_menu()
        selected_option = int(input())
        return self.options_dict[selected_option].invoke()

    def print_menu(self):
        print("1. {}".format(self.options_dict[1].message))
        print("2. {}".format(self.options_dict[2].message))
        print("0. {}".format(self.options_dict[0].message))

    def _handle_account_creation(self):
        return self.bs.create_account()

    def _handle_login(self):
        return self.bs.handle_login()

    def _handle_exit(self):
        return ExitMenu(self.bs)


class AccountMenu(GenericMenu):

    def __init__(self, bs: BankingSystem):
        super().__init__(bs)
        self.options_dict = {1: MenuItem("Balance", self._handle_balance_check),
                             2: MenuItem("Log out", self._handle_logout),
                             0: MenuItem("Exit", self._handle_exit)}

    def print_menu(self):
        print("1. {}".format(self.options_dict[1].message))
        print("2. {}".format(self.options_dict[2].message))
        print("0. {}".format(self.options_dict[0].message))

    def wait_for_input(self):
        self.print_menu()
        selected_option = int(input())
        return self.options_dict[selected_option].invoke()

    def _handle_balance_check(self):
        return self.bs.check_current_account_balance()

    def _handle_logout(self):
        return self.bs.handle_logout()

    def _handle_exit(self):
        return ExitMenu(self.bs)


def run():
    banking_system = BankingSystem()
    menu = MainMenu(bs=banking_system)
    while True:
        menu = menu.wait_for_input()


run()
