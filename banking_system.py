

class BankingSystem:

    def __init__(self, account_generator, repository):
        self.current_account = None  # create a null object

        self.account_generator = account_generator
        self.repository = repository

    def create_account(self):
        last_account_id = self._get_last_account_id()
        acc = self.account_generator.generate_account(last_account_id)
        acc.save(self.repository)
        acc.print_account_credentials()

    def handle_login(self):
        card_number = input("Enter your card number:")
        card_pin = input("Enter your PIN:")
        self._try_login(card_number, card_pin)

    def check_current_account_balance(self):
        print(self.repository.get_account_balance(self.current_account.card_number))

    def handle_logout(self):
        self.current_account = None  # create null object

    # TODO: extract and simplify
    def _try_login(self, card_number, pin):
        account = self.repository.find_account_by_card_number(card_number)
        # TODO: there's a bug here - sometimes the pin validation fails
        if account and account.card_number == card_number and account.pin == pin:
            print("You have successfully logged in!")
            self.current_account = account
        else:
            raise WrongAccountNumberException()

    def _get_last_account_id(self):
        return self.repository.find_last_added_card_number()

    def add_income(self):
        print("Enter income:")
        income = int(input())
        self.current_account = self.current_account.add_income(income, self.repository)
        print("Income was added!")

    # TODO: extract and simplify
    def transfer_money(self):
        print("Enter card number:")
        card_number = input()
        if card_number == self.current_account.card_number:
            print("You can't transfer money to the same account!")
            return
        elif self._is_entered_card_number_valid(card_number):
            print("Probably you made a mistake in the card number. Please try again!")
            return
        target_account = self.repository.find_account_by_card_number(card_number)
        if not target_account:
            print("Such a card does not exist.")
            return
        print("Enter how much money you want to transfer:")
        money_to_transfer = int(input())
        if self.current_account.balance < money_to_transfer:
            print("Not enough money!")
            return
        self.current_account.add_income(money_to_transfer * -1, self.repository)
        target_account.add_income(money_to_transfer, self.repository)
        print("Success!")

    def _is_entered_card_number_valid(self, card_number):
        generated_checksum = self.account_generator.generate_checksum(card_number[:-1])
        stored_checksum = int(card_number[-1])
        return generated_checksum == stored_checksum

    def close_account(self):
        self.repository.delete_card_by_card_number(self.current_account.card_number)


class WrongAccountNumberException(Exception):
    pass
