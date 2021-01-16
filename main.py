import random
import sqlite3
import sys


class BankingSystem:

    def __init__(self, account_generator, repository):
        self.accounts = {}
        self.current_account = None  # create a null object
        self.account_generator = account_generator
        self.repository = repository

    def create_account(self):
        last_account_id = self._get_last_account_id()
        acc = self.account_generator.generate_account(last_account_id)
        acc.save(self.repository)
        self.accounts[acc.card_number] = acc
        acc.print_account_credentials()
        return MainMenu(self)

    def handle_login(self):
        card_number = input("Enter your card number:")
        card_pin = input("Enter your PIN:")
        return self._try_login(card_number, card_pin)

    def check_current_account_balance(self):
        print(self.repository.get_account_balance(self.current_account.card_number))
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

    def _get_last_account_id(self):
        return self.repository.find_last_added_card_number()


class AccountId:
    MIN_LENGTH = 9
    MAX_LENGTH = 12  # not used yet

    def __init__(self, number=0, string_value="000000000") -> None:
        self._current_number = number
        self.str_value = string_value

    @staticmethod
    def from_card_number(card_number):
        account_id_with_checksum = card_number[len("400000"):]
        bare_account_id = account_id_with_checksum[:-1]
        account_number = int(bare_account_id)
        return AccountId(account_number, bare_account_id)

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

    def generate_account(self, last_account_id):
        account_id = last_account_id.increment()
        card_number = self._generate_card_number(account_id.str_value)
        pin_number = self._generate_pin()
        new_account = Account(card_number, pin_number)
        return new_account

    def _generate_pin(self):
        pin = ""
        for i in range(4):
            pin += str(random.randint(0, 9))
        return pin

    def _generate_card_number(self, unique_account_id):
        checksum = self.generate_checksum("400000" + unique_account_id)
        return "400000{}{}".format(unique_account_id, checksum)

    def generate_checksum(self, unique_account_id):
        number_array = []
        for idx, number in enumerate(unique_account_id):
            number = int(number)
            if (idx + 1) % 2 != 0:
                number *= 2
            number_array.append(number)

        for idx, element in enumerate(number_array):
            if element > 9:
                element -= 9
            number_array[idx] = element

        checksum = (10 - (sum(number_array) % 10)) % 10
        return checksum


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

    def save(self, repository):
        repository.save_account_data(self.card_number, self.pin, self.balance)


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
        return self.bs.check_current_account_balance()

    def _handle_logout(self):
        return self.bs.handle_logout()

    def _handle_exit(self):
        return ExitMenu(self.bs)


class MultiPurposeRepository:

    def __init__(self, db_connection):
        self.connection = db_connection

    def get_last_account(self):
        pass  # implement

    def initialize_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS card(id INTEGER primary key, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
        self.connection.commit()

    def save_account_data(self, number, pin, balance):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO card(number, pin, balance) values ({0}, {1}, {2})".format(
            number, pin, balance
        ))
        self.connection.commit()

    def get_account_balance(self, number):
        cursor = self.connection.cursor()
        cursor.execute("SELECT balance FROM card WHERE number = '{0}'".format(number))
        return cursor.fetchone()[0]

    def find_last_added_card_number(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT number from card ORDER BY id DESC LIMIT 1")
        entry = cursor.fetchone()
        if entry:
            return AccountId.from_card_number(entry[0])
        else:
            return AccountId()

    def find_all_accounts(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM accounts")
        print(cursor.fetchone())


def run():
    db_connection = sqlite3.connect("card.s3db")
    repo = MultiPurposeRepository(db_connection)
    repo.initialize_tables()
    banking_system = BankingSystem(AccountGenerator(), repo)
    menu = MainMenu(bs=banking_system)
    while True:
        menu = menu.wait_for_input()


run()
