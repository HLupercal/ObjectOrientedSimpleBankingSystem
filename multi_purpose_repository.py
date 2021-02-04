from account import AccountId, Account


class MultiPurposeRepository:

    def __init__(self, db_connection):
        self.connection = db_connection

    def initialize_tables(self):
        cursor = self.connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS card(id INTEGER primary key, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
        self.connection.commit()

    def find_account_by_card_number(self, card_number):
        """

        :param card_number: string
        :return: Either AccountId object or None
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT number, pin, balance FROM card WHERE number={0}".format(
            card_number
        ))
        entry = cursor.fetchone()
        if entry:
            return Account(entry[0], entry[1], entry[2])
        else:
            None

    def save_account_data(self, number, pin, balance):  # change arg to account
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO card(number, pin, balance) values ({0}, {1}, {2})".format(
            number, pin, balance
        ))
        self.connection.commit()

    def update_account_balance(self, card_number, balance):  # change arg to account
        cursor = self.connection.cursor()
        cursor.execute("UPDATE card SET balance = {0} WHERE number = {1}".format(
            balance, card_number
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

    def delete_card_by_card_number(self, card_number):
        cursor = self.connection.cursor()
        cursor.execute("DELETE from card WHERE number='{0}'".format(card_number))
        self.connection.commit()