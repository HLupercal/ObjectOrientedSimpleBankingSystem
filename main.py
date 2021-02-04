import sqlite3

from account import AccountGenerator
from menus import MainMenu
from banking_system import BankingSystem
from multi_purpose_repository import MultiPurposeRepository


def run():
    db_connection = sqlite3.connect("card.s3db")
    repo = MultiPurposeRepository(db_connection)
    repo.initialize_tables()
    banking_system = BankingSystem(AccountGenerator(), repo)
    menu = MainMenu(bs=banking_system)
    while True:
        menu = menu.wait_for_input()


run()
