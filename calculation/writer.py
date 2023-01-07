import xlsxwriter
from datastructures import Stack
from datastructures import Queue

# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]

# Transaction_profits: {[currency]: [date, profit], ...}
# Currency_profits: {[currency]: profit, ...}

def write_to_excel(transactions, amounts, transaction_profits, transaction_currency_profits, currency_profits):

    # Initialization
    workbook, transactions_sheet, results_sheet, assets_sheet = initialize_workbook_and_worksheets()
    
    # Formatting
    format = get_format(workbook)
    
    # Create charts
    bar_chart = get_bar_chart(workbook)
    pie_chart = get_pie_chart(workbook)

    # Fix worksheets
    write_transactions_sheet(transactions_sheet, transactions, transaction_profits, format)
    write_results_sheet(results_sheet, currency_profits, format, bar_chart)
    write_assets_sheet(assets_sheet, transactions, amounts, currency_profits, format, pie_chart)

    # Profit per transaction
    # - Write each transaction to a new line in excel
    # - Write each transaction_profit to a new line in excel
    # TODO: Fix



    # Assets and total profit per currency
    # - Write each transaction to a new line in excel (debit/credit per currency)
    # - Write currency_profit per currency

    workbook.close()

    return None

def write_transactions_sheet(sheet, transactions, transactions_profits, format):
    
    # Write headers
    sheet.write('B2', "Transactions", format["sheet_header"])
    sheet.write('B4', "Date", format["column_header"])
    sheet.write('C4', "Currency Sold", format["column_header"])
    sheet.write('D4', "Amount Sold", format["column_header"])
    sheet.write('E4', "Price Sold", format["column_header"])
    sheet.write('F4', "Currency Bought", format["column_header"])
    sheet.write('G4', "Amount Bought", format["column_header"])
    sheet.write('H4', "Price Bought", format["column_header"])
    sheet.write('I4', "Profit", format["column_header"])
    
    # Set column-width
    sheet.set_column(1, 1, 12)
    sheet.set_column(2, 2, 15, format["center_align"])
    sheet.set_column(3, 3, 12)
    sheet.set_column(4, 4, 12)
    sheet.set_column(5, 5, 17, format["center_align"])
    sheet.set_column(6, 6, 15)
    sheet.set_column(7, 7, 12)
    sheet.set_column(8, 8, 10, format["center_align"])
    
    # Set conditional format when profit > 0
    sheet.conditional_format('I5:I200', {
                                            'type': 'cell',
                                            'criteria': '>',
                                            'value': 0,
                                            'format': format["green"]})
    
    # Set conditional format when profit < 0
    sheet.conditional_format('I5:I200', {
                                            'type': 'cell',
                                            'criteria': '<',
                                            'value': 0,
                                            'format': format["red"]})
    
    # Write transactions
    row = 5                                # Starts at row 5 (+1)
    for transaction in transactions:
        sheet.write('B' + str(row), transaction[transaction_index["date"]])
        sheet.write('C' + str(row), transaction[transaction_index["currency_sold"]])
        sheet.write('D' + str(row), transaction[transaction_index["amount_sold"]])
        sheet.write('E' + str(row), transaction[transaction_index["price_sold"]])
        sheet.write('F' + str(row), transaction[transaction_index["currency_bought"]])
        sheet.write('G' + str(row), transaction[transaction_index["amount_bought"]])
        sheet.write('H' + str(row), transaction[transaction_index["price_bought"]])
        sheet.write('I' + str(row), transactions_profits[row - 5])                       # List starts at index 0
        row += 1
    
    print('Transaction sheet completed.')    
    
    return None

def write_results_sheet(sheet, currency_profits, format, bar_chart):
    
    # Write headers
    sheet.write('B2', "Results", format["sheet_header"])
    sheet.write('B4', "Currency", format["column_header"])
    sheet.write('C4', "Profit", format["column_header"])
    
    # Set column-width
    sheet.set_column(1, 1, 12)
    sheet.set_column(2, 2, 15, format["center_align"])
    
    # Set conditional format when profit > 0
    sheet.conditional_format('C5:C200', {
                                            'type': 'cell',
                                            'criteria': '>',
                                            'value': 0,
                                            'format': format["green"]})
    
    # Set conditional format when profit < 0
    sheet.conditional_format('C5:C200', {
                                            'type': 'cell',
                                            'criteria': '<',
                                            'value': 0,
                                            'format': format["red"]})
    
    # Write profit of currencies
    row = 5         # Starts at row 6 (5+1)
    for currency, profit in currency_profits.items():
        sheet.write('B' + str(row), currency)
        sheet.write('C' + str(row), profit)
        row += 1
    
    # Add series to the bar chart
    bar_chart.add_series({
        'name': '=Results!$B$2',
        'categories': '=Results!$B$5:$B$' + str(row),
        'values': '=Results!$C$5:$C$' + str(row),
        'data_labels': {'value': True, 'num_format': '#,##0.00'}
    })
    
    # Insert chart into sheet
    sheet.insert_chart('D4', bar_chart)
    
    print('Results sheet completed.')   
    
    return None

def write_assets_sheet(sheet, transactions, amounts, currency_profits, format, pie_chart):
    
    # Update assets per transaction
    # Show sum of assets after all transactions
    # Allow for initial asset inputs?
    
    # Write headers
    sheet.write('B2', "Assets", format["sheet_header"])
    sheet.write('B4', "Currency", format["column_header"])
    sheet.write('C4', "Amount", format["column_header"])
    
    # Set column-width
    sheet.set_column(1, 1, 12)
    sheet.set_column(2, 2, 15, format["center_align"])
    
    # Write amount of currencies
    row = 5         # Starts at row 6 (5+1)
    for currency, amount in amounts.items():
        sheet.write('B' + str(row), currency)
        sheet.write('C' + str(row), amount.dequeue()[amount_index['amount']])
        row += 1
    
    # TODO: Use get_price() to get current value of amounts, use values to create pie chart
    
    # Add series to the pie chart
    pie_chart.add_series({
        'name': '=Assets!$B$2',
        'categories': '=Assets!$B$5:$B$' + str(row),
        'values': '=Assets!$C$5:$C$' + str(row),
        'data_labels': {'value': True, 'num_format': '#,##0.00'}
    })
    
    # Insert chart into sheet
    sheet.insert_chart('D4', pie_chart)
    
    print('Assets sheet completed.') 
    
    return None

# Define transaction
transaction_index = {
    "date": 0,
    "currency_sold": 1,
    "amount_sold": 2,
    "price_sold": 3,
    "currency_bought": 4,
    "amount_bought": 5,
    "price_bought": 6
}

# Define amounts
amount_index = {
    "date": 0,
    "amount": 1
}

### Helper Methods ###
def initialize_workbook_and_worksheets():
    workbook = xlsxwriter.Workbook('tax_info.xlsx')
    transactions_sheet = workbook.add_worksheet('Transactions')
    results_sheet = workbook.add_worksheet('Results')
    assets_sheet = workbook.add_worksheet('Assets')
    
    return workbook, transactions_sheet, results_sheet, assets_sheet

def get_format(workbook):
    
    format = {
        "sheet_header": workbook.add_format({'bold': 1, 'font_size': 14}),
        "column_header": workbook.add_format({'bold': 1, 'bottom': 1}),
        "center_align": workbook.add_format({'align': 'center'}),
        "green": workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'}),
        "red": workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    }

    return format

def get_bar_chart(workbook):
    
    return workbook.add_chart({'type': 'bar'})

def get_pie_chart(workbook):
    
    return workbook.add_chart({'type': 'pie'})


### Testing ###

# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
cleaned_transaction_1 = ["01/01/2023", "BTC", 0.5, 25000, "USD", 12500, 1]
cleaned_transaction_2 = ["02/01/2023", "USD", 5000, 1, "BTC", 0.25, 20000]
cleaned_transactions = [cleaned_transaction_1, cleaned_transaction_2]

amounts = {"BTC": Stack()}
amounts["BTC"].enqueue(["01/01/2023", 0.25])
transaction_profits = [10000, 0]
transaction_currency_profits = {"BTC": ["01/01/2023", 10000]}
currency_profits = {"BTC": 10000, "ETH": -5000}

write_to_excel(cleaned_transactions, amounts, transaction_profits, transaction_currency_profits, currency_profits)





