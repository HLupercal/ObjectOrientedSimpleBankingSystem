import sys
from abc import ABC, abstractmethod

from banking_system import BankingSystem, WrongAccountNumberException


class MenuItem:

    def __init__(self, message, handler_function):
        self.message = message
        self.handler_function = handler_function

    def invoke(self):
        return self.handler_function()


class GenericMenu(ABC):
    def __init__(self, bs: BankingSystem):
        self.bs = bs

    @abstractmethod
    def wait_for_input(self):
        ...


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
        self.bs.create_account()
        return MainMenu(self.bs)

    def _handle_login(self):
        try:
            self.bs.handle_login()
            return AccountMenu(self.bs)
        except WrongAccountNumberException:
            print("Wrong card number or PIN!")
            return MainMenu(self.bs)

    def _handle_exit(self):
        return ExitMenu(self.bs)


class AccountMenu(GenericMenu):

    def __init__(self, bs: BankingSystem):
        super().__init__(bs)
        self.options_dict = {1: MenuItem("Balance", self._handle_balance_check),
                             2: MenuItem("Add Income", self._handle_add_income),
                             3: MenuItem("Do Transfer", self._handle_transfer),
                             4: MenuItem("Close Account", self._handle_close_account),
                             5: MenuItem("Log out", self._handle_logout),
                             0: MenuItem("Exit", self._handle_exit)}

    def print_menu(self):
        print("1. {}".format(self.options_dict[1].message))
        print("2. {}".format(self.options_dict[2].message))
        print("3. {}".format(self.options_dict[3].message))
        print("4. {}".format(self.options_dict[4].message))
        print("5. {}".format(self.options_dict[5].message))
        print("0. {}".format(self.options_dict[0].message))

    def wait_for_input(self):
        self.print_menu()
        selected_option = int(input())
        return self.options_dict[selected_option].invoke()

    def _handle_balance_check(self):
        self.bs.check_current_account_balance()
        return AccountMenu(self.bs)

    def _handle_add_income(self):
        self.bs.add_income()
        return AccountMenu(self.bs)

    def _handle_transfer(self):
        self.bs.transfer_money()
        return AccountMenu(self.bs)

    def _handle_close_account(self):
        self.bs.close_account()
        return MainMenu(self.bs)

    def _handle_logout(self):
        self.bs.handle_logout()
        return MainMenu(self.bs)

    def _handle_exit(self):
        return ExitMenu(self.bs)
