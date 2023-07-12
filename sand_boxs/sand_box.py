
import os
import shutil
from journal_manager import JournalManager
from trade import Trade
import pandas as pd
import queue


journal_filename = "trading_journal.xlsx"
journal_model_path = os.getcwd() + r"\config\trading_journal_model.xlsx"
default_journal_path = os.getcwd()

LOG_FIRST_COL_NAME = 'Stock'
NUM_LINES_FIELD = 2 # Can't be modified only from here.

# def find_start_log_fields(log_table):
#     start_row_idx, start_col_idx = None, None
#     for i, row in log_table.iterrows():
#         for j, value in enumerate(row):
#             if value == LOG_FIRST_COL_NAME:
#                 start_row_idx = i
#                 start_col_idx = j
#                 break
#     return start_row_idx, start_col_idx
#
#
#
# def get_field_dict(log_tabel, start_row_idx, start_col_idx):
#     dict_fields = {}
#     temp_value = ''
#     first_nan = True
#
#     for j, value in enumerate(log_tabel.iloc[start_row_idx, start_col_idx:], start=start_col_idx):
#         if pd.isna(value):
#             if first_nan:
#                 dict_fields[temp_value] = [log_tabel.iloc[start_row_idx+1, j-1]]
#                 first_nan = False
#             dict_fields[temp_value].append(log_tabel.iloc[start_row_idx+1, j])
#         else:
#             dict_fields[value] = None
#             temp_value = value
#             first_nan = True
#
#     return dict_fields


def main():
    pass

    #manager = JournalManager()
    #print(manager.trade_fields_tostring())
    #trade = Trade(manager)
    #trade.Entry_Label = "hello"
    #print(trade.Stock)
    #print(trade.trade_attr_tostring())
    #print(trade.Entry_Label)





    #log_table = pd.read_excel(journal_filename)
    # 22222222222222222222222

    #start_row_idx, start_col_idx = find_start_log_fields(log_table)
    #fields_dict = get_field_dict(log_table, start_row_idx, start_col_idx)

    # 111111111111111111111111

    # manager = JournalManager(r"C:\Users\user\Desktop\Cloud Files\TradingTools\trade_journal_project\sand_box_temp\trading_journal.xlsx")
    # print(manager.journal_path)
    # print("\n\n\nPassing file to a different directory.......")
    # manager.journal_path = r"C:\Users\user\Desktop\Cloud Files\TradingTools\trade_journal_project\sand_box_temp\trading_journal.xlsx"
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