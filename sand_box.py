
import os
import shutil
from journal_manager import journal_manager


journal_filename = "trading_journal.xlsx"
journal_model_path = os.getcwd() + r"\config\trading_journal_model.xlsx"
default_journal_path = os.getcwd()

def main():
    print("hello")
























    # manager = journal_manager(r"C:\Users\user\Desktop\Cloud Files\TradingTools\trade_journal_project\sand_box_temp\trading_journal.xlsx")
    # print(manager.journal_path)
    # print("\n\n\nPassing file to a different directory.......")
    # manager.journal_path = r"C:\Users\user\Desktop\Cloud Files\TradingTools\trade_journal_project\sand_box_temp"
    # print(manager.journal_path)


    # global journal_filename, journal_model_path
    # global default_journal_path
    # path = input("what is the path to the Journal? :    ")
    # filepath = os.path.join(path, journal_filename)
    # if os.path.isfile(filepath):
    #     print("Journal Is Already exists. No need to create a new one.")
    # else:
    #     print("Building Trading Journal in given path.\n\nJournal name: " + journal_filename)
    #     shutil.copy(journal_model_path, filepath)
















if __name__ == '__main__':
    main()