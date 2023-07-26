Dim xlApp, xlBook, xlSheet

On Error Resume Next
Set xlApp = GetObject(, "Excel.Application") ' looking for open excel application
On Error GoTo 0

If xlApp Is Nothing Then ' If no excel application is open generate an error
    MsgBox "Excel is not running. Please open Excel and try again.", vbExclamation
    WScript.Quit
End If

Set xlBook = xlApp.Workbooks("trading_journal.xlsx") ' Opening the trading_journal workbook
Set xlSheet = xlBook.Worksheets("Trade Log") ' Use the appropriate sheet index or name

' Write data to random cell
xlSheet.Cells(9, 3).Value = "Hello, Excel!"

' Save the changes (optional)
xlBook.Save

' Close the workbook (optional)
' xlBook.Close

' Quit Excel (optional)
' xlApp.Quit

Set xlSheet = Nothing
Set xlBook = Nothing
Set xlApp = Nothing





' On Error Resume Next
' Dim xlApp
' Set xlApp = GetObject(, "Excel.Application")
' On Error GoTo 0

' If xlApp Is Nothing Then
'     MsgBox "Excel is not running. Please open Excel and try again.", vbExclamation
'     WScript.Quit
' End If

' Dim xlBook
' On Error Resume Next
' Set xlBook = xlApp.Workbooks("your_file.xlsx")
' On Error GoTo 0

' If xlBook Is Nothing Then
'     MsgBox "Workbook 'your_file.xlsx' not found. Please ensure it is open and try again.", vbExclamation
'     WScript.Quit
' End If

' ' Find the sheet by name
' Dim sheetName
' sheetName = "Sheet1" ' Replace "Sheet1" with the name of the sheet you want to access

' Dim xlSheet
' For Each xlSheet In xlBook.Worksheets
'     If xlSheet.Name = sheetName Then
'         Set xlSheet = xlSheet ' Found the sheet by name
'         Exit For
'     End If
' Next

' If xlSheet Is Nothing Then
'     MsgBox "Sheet '" & sheetName & "' not found in the workbook.", vbExclamation
'     WScript.Quit
' End If

' ' Now you have the reference to the sheet by name in the variable xlSheet
' ' You can interact with the sheet using xlSheet object

' ' For example, writing data to cell A1:
' xlSheet.Cells(1, 1).Value = "Hello, Sheet1!"

' ' Save changes and clean up resources if needed
' xlBook.Save
' xlBook.Close
' xlApp.Quit

' Set xlSheet = Nothing
' Set xlBook = Nothing
' Set xlApp = Nothing
