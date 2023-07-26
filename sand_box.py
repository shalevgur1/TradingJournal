from journal_manager import JournalManager
import pandas as pd

import xlwings as xw

def write_to_excel(file_path, data):
    # Create an Excel App object
    app = xw.App(visible=False)  # Set visible=True if you want to see Excel during execution

    try:
        # Open the workbook or create a new one if it doesn't exist
        workbook = xw.Book(file_path)
        sheet = workbook.sheets["Trade Log"]  # Assuming you want to write to the first sheet

        # Write data to Excel
        sheet.range('D11').value = data

        # Save changes and close the workbook
        workbook.save()
        #workbook.close()

    except Exception as e:
        print("\nError:", e)

    print("\nData written to Excel successfully.")

    # finally:
    #     # Close the Excel App object
    #     app.quit()

def write_value(trade_log_sheet, trade_journal, col:chr, row:int, value):
    """
    Gets a row and a colum and a value and write it to the trade journal
    """
    trade_log_sheet.range(col+str(row)).value = str(value)
    trade_journal.save()

def main():
    # # Example data to be written to Excel
    # data_to_write = [
    #     [1, 'John', 100],
    #     [2, 'Alice', 150],
    #     [3, 'Bob', 200]
    # ]

    # # Specify the file path where you want to write the data
    # file_path = r"C:\Users\user\Desktop\Cloud Files\TradingTools\trade_journal_project\trading_journal.xlsx"

    # # Call the function to write data to Excel
    # write_to_excel(file_path, data_to_write)

    log_data = pd.read_excel(r"C:\Users\user\Desktop\Cloud Files\TradingTools\trade_journal_project\trading_journal.xlsx")
    app = xw.App(visible=False)
    workbook = xw.Book(r"C:\Users\user\Desktop\Cloud Files\TradingTools\trade_journal_project\trading_journal.xlsx")
    sheet = workbook.sheets["Trade Log"]  # Assuming you want to write to the first sheet
    write_value(sheet, workbook, 'C', 5, 'value')




if __name__ == '__main__':
    main()