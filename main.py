import random
import sys


class BankingSystem:

    def __init__(self, account_generator):
        self.accounts = {}
        self.current_account = None  # create a null object
        self.account_generator = account_generator

    def create_account(self):
        acc = self.account_generator.generate_account()
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


class AccountId:
    MIN_LENGTH = 9
    MAX_LENGTH = 12

    def __init__(self, number=0, string_value="000000000") -> None:
        self._current_number = number
        self.str_value = string_value

    def get_value(self):
        return self.str_value

    def increment(self):
        new_number = self._current_number + 1
        str_value = self._pad_with_zeroes(new_number)
        return AccountId(new_number, str_value)

    def _pad_with_zeroes(self, new_number):
        new_number_as_string = str(new_number)
        length = len(new_number_as_string)
        if len(str(new_number)) < self.MIN_LENGTH:
            number_of_zeroes = self.MIN_LENGTH - length
            new_number_as_string = "{}{}".format("0" * number_of_zeroes, new_number)
        return new_number_as_string


class AccountGenerator:

    def __init__(self):
        self.last_account_id = AccountId()

    def generate_account(self):
        account_id = self.last_account_id.increment()
        card_number = self._generate_card_number(account_id.str_value)
        pin_number = self._generate_pin()
        new_account = Account(card_number, pin_number)
        self._update_last_unique_id(account_id)  # update unique id only when account created successfully
        return new_account

    def _generate_pin(self):
        pin = ""
        for i in range(4):
            pin += str(random.randint(0, 9))
        return pin

    def _generate_card_number(self, unique_account_id):
        checksum = self.generate_checksum()
        return "400000{}{}".format(unique_account_id, checksum)

    def _update_last_unique_id(self, account_id):
        self.last_account_id = account_id

    def generate_checksum(self):
        return 0


class Account:

    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin
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
    banking_system = BankingSystem(AccountGenerator())
    menu = MainMenu(bs=banking_system)
    while True:
        menu = menu.wait_for_input()


run()
