
import os
import shutil
import pandas as pd
import xlwings as xw

# from trade import Trade # Creates a circular import



class JournalManager:
    """
    This Class is manege the Excel file Trading Journal
    It do various of things:
    1. Building the Trading Journal
    2. Extracting and inserting data to the Journal.
    """

    _DEFAULT_PATH = os.getcwd()                                         # Journal default path in the script directory
    _MODEL_PATH = os.getcwd() + r"\config\trading_journal_model.xlsx"   # Journal config/model file full path
    _LOG_FIRST_FIELD_NAME = 'Stock'                                     # The name of the first field in log table

    _journal_filename = "trading_journal.xlsx"                          # Journal file name
    _journal_path = ''                                                  # Journal file full path

    _log_data = None                    # The log table data from log sheet in the Journal file
    trade_fields = {}                   # A dict that contains all the fields of a trade taken from Trade Log sheet

    _excel_app = None                        # The Excel application object
    _journal_workbook = None                 # Trade Journal Excel Workbook obeject
    _log_sheet = None                  # Trade Log Excel Sheet object
    _first_col_log = ''                      # The first col of the Trade Log - char value
    _first_empty_row_log = 5                 # The last empty row to start write trades too. By default the first row in the Journal (change in the init)


    def __init__(self, journal_path=_DEFAULT_PATH):
        """
        Build Journal in given path. By default the path is 
        the Current Working Directory of the application
        """
        # Building the Journal File
        if self._journal_filename not in journal_path:
            journal_path = os.path.join(journal_path, self._journal_filename)
        self.build_journal(journal_path)

        # Creating the _trade_fields dict
        self._read_log_table()
        self._read_trade_fields()

        # Find first colum of the Trade Log
        _, first_col = self.get_start_fields_idx()
        self._first_col_log = self._find_col_char(first_col)
        # Finding the first empty row in Trade Log
        self._find_next_row()



    def build_journal(self, journal_file_path):
        """
        Building the journal in a given folder path if not exists already
        """
        if os.path.isfile(journal_file_path):
            print("Trading Journal is already exists.")
        else:
            print("Creating Trading Journal file...\n"
                  "In Path: " + journal_file_path)
            shutil.copy(self._MODEL_PATH, journal_file_path)
        self._journal_path = journal_file_path

        # Initialize the trade_journal object and different sheets that is used to interact with the Journal
        # self._excel_app_object = xw.App(visible=False) # If necessary to initialize the excel application
        self._journal_workbook = xw.Book(journal_file_path)
        self._log_sheet = self._journal_workbook.sheets["Trade Log"]


    def transport_journal(self, new_path):
        """
        Pass the Journal to a different directory.
        DOES NOT DELETE THE OLD PATH FILE
        """
        if os.path.isfile(new_path):
            print("File already exists in given folder......")
        else:
            shutil.copy(self._journal_path, new_path)

    def _read_log_table(self):
        """
        Reads the log table sheet in the
        Journal Excel file to a pandas dataFrame property
        """
        self._log_data = pd.read_excel(self._journal_path)

    def _read_trade_fields(self):
        """
        This function is extracting the fields of a trade
        from the Excel Journal file.
        This is for convenience - when changing config file,
        everything will change accordingly
        Used in Trade Class
        Creating a dictionary of the fields.
        """
        self.check_read_log()

        dict_fields = {}
        temp_value = ''
        first_nan = True
        start_row_idx, start_col_idx = self.get_start_fields_idx()

        # Iterating over _log_data dataFrame on fields lines.
        # For every field with sub-fields -
        # create a list with all sub-fields while field is the dict key.
        for j, value in enumerate(self._log_data.iloc[start_row_idx, start_col_idx:], start=start_col_idx):
            if pd.isna(value):
                if first_nan:
                    dict_fields[temp_value] = [self._log_data.iloc[start_row_idx + 1, j - 1]]
                    first_nan = False
                dict_fields[temp_value].append(self._log_data.iloc[start_row_idx + 1, j])
            else:
                dict_fields[value] = None
                temp_value = value
                first_nan = True

        self.trade_fields = dict_fields

    def _find_next_row(self):
        """
        Finds the first empty row to write to
        """
        counter = self._first_empty_row_log  # Initialized to the first row
        while True:
            cell_name = self._first_col_log + str(counter)
            cell_value = self._log_sheet.range(cell_name).value
            if not cell_value:
                self._first_empty_row_log = counter
                break
            counter += 1

    def _find_col_char(self, col_number):
        """
        Finds the specified colum of the Trade Log by number.
        returns a char representing the colum number in excel.
        """
        char_counter = col_number + 1
        colum_char = ''
        while char_counter > 0:
            char_counter, remainder = divmod(char_counter, 26)
            if remainder == 0:
                remainder = 26
            colum_char = chr(64 + remainder) + colum_char

        return colum_char

    def trade_fields_tostring(self):
        """
        Creates a string from Trade Log table fields.
        Using the trade_fields Dictionary.
        """
        fields_str = ''
        for key, value in self.trade_fields.items():
            fields_str = fields_str + key
            if value is not None:
                fields_str = fields_str + ': | '
                for sub_val in self.trade_fields[key]:
                    fields_str = fields_str + sub_val + ' | '
            fields_str = fields_str + '\n'

        return fields_str

    def get_start_fields_idx(self):
        """
        Returns the index (row and col) of the first (upper left) field in the Log Table
        """
        self.check_read_log()
        idx_found = False
        start_row_idx, start_col_idx = None, None
        for i, row in self._log_data.iterrows():
            for j, value in enumerate(row):
                if value == self._LOG_FIRST_FIELD_NAME:
                    start_row_idx = i
                    start_col_idx = j
                    idx_found = True
                    break
            if idx_found:
                break
        return start_row_idx, start_col_idx

    def check_read_log(self):
        """
        Check that the log data property has data and
        the log table sheet has been read.
        """
        if self._log_data is None or self._log_data.empty:
            raise ValueError("Log Table has not been read yet or log data is empty for some reason")

    @property
    def journal_path(self):
        return self._journal_path

    @journal_path.setter
    def journal_path(self, path):
        answer = input("Are you sure you want to path the Journal file to a different directory?")
        if answer in ["yes", "Yes", "y", "Y"]:
            if self._journal_filename not in path:
                path = os.path.join(path, self._journal_filename)
            self.transport_journal(path)
            self._journal_path = path

    def _write_value(self,workbook, sheet, col:chr, row:int, value):
        """
        Gets a row and a colum and a value and write it to the trade journal
        """
        sheet.range(col+str(row)).value = str(value)
        workbook.save()

    def write_trade(self, trade):
        """
        Gets a trade object with relevant data and 
        write its contents to the trade journal
        """

        # Creating temp access to the Trade Journal because 
        # multi-threaded environment binding different xw objects for every thread
        temp_journal_workbook = xw.Book(self._journal_path)
        temp_log_sheet = temp_journal_workbook.sheets["Trade Log"]

        _, col_counter = self.get_start_fields_idx()
        for attr, value_or_subattr in trade.trade_fields_attr.items():

            # Check if has subfields
            if isinstance(value_or_subattr, list):
                for subattr in value_or_subattr:
                    value = getattr(getattr(trade, attr), subattr)
                    if value:
                        # Print value to excel file
                        self._write_value(temp_journal_workbook, temp_log_sheet, self._find_col_char(col_counter), self._first_empty_row_log, value)
                    col_counter += 1
            # Has no subfields
            else:
                value = getattr(trade, attr)
                if value:
                    # Print value to excel file
                    self._write_value(temp_journal_workbook, temp_log_sheet, self._find_col_char(col_counter), self._first_empty_row_log, value)
                col_counter += 1
        self._first_empty_row_log += 1