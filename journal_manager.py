
import os
import shutil


# This Class is mange the Excel file Trading Journal
# It do various of things:
# 1. Building the Trading Journal
# 2. Extracting and inserting data to the Journal.
class journal_manager:

    _DEFAULT_PATH = r'C:\Users\user\Desktop\Cloud Files\TradingTools\trade_journal_project'
    _MODEL_PATH = os.getcwd() + r"\config\trading_journal_model.xlsx"

    _journal_filename = "trading_journal.xlsx"
    _journal_path = ''

    def __init__(self, journal_path=_DEFAULT_PATH):
        if self._journal_filename not in journal_path:
            journal_path = os.path.join(journal_path, self._journal_filename)
        self.build_journal(journal_path)

    # Building the journal in a given folder path if not exists already
    def build_journal(self, journal_file_path):
        if os.path.isfile(journal_file_path):
            print("Trading Journal is already exists.")
        else:
            print("Creating Trading Journal file...\n"
                  "In Path: " + journal_file_path)
            shutil.copy(self._MODEL_PATH, journal_file_path)
        self._journal_path = journal_file_path

    # Pass the Journal to a different directory.
    # DOES NOT DELETE THE OLD PATH FILE
    def transport_journal(self, new_path):
        if os.path.isfile(new_path):
            print("File already exists in given folder......")
        else:
            shutil.copy(self._journal_path, new_path)

    @property
    def journal_path(self):
        return self._journal_path

    @journal_path.setter
    def journal_path(self, path):
        answer = input("Are you sure you want to path the Jouranl file to a different directory?")
        if answer in ["yes", "Yes", "y", "Y"]:
            if self._journal_filename not in path:
                path = os.path.join(path, self._journal_filename)
            self.transport_journal(path)
            self._journal_path = path