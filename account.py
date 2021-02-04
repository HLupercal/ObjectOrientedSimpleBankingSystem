import random


class AccountId:
    MIN_LENGTH = 9

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

    def __init__(self, card_number, pin, balance=0):
        self.card_number = card_number
        self.pin = pin
        self.balance = balance

    def print_account_credentials(self):
        print("Your card has been created")
        print("Your card number:")
        print(self.card_number)
        print("Your card PIN:")
        print(self.pin)

    def add_income(self, income, repository):
        self.balance += income
        repository.update_account_balance(self.card_number, self.balance)
        return self

    def save(self, repository):
        repository.save_account_data(self.card_number, self.pin, self.balance)

