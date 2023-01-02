import xlsxwriter

# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]

# Transaction_profits: {[currency]: [date, profit], ...}
# Currency_profits: {[currency]: profit, ...}

def write_to_excel(transactions, transaction_profits, currency_profits):

    # Initialization
    workbook, transactions_sheet, assets_sheet = initialize_workbook_and_worksheets()
    
    # Formatting
    format = {
        "sheet_header": workbook.add_format({'bold': 1, 'font_size': 14}),
        "column_header": workbook.add_format({'bold': 1, 'bottom': 1})
    }

    # Fix worksheets
    write_transactions_sheet(transactions, transaction_profits, transactions_sheet, format)
    write_assets_sheet(transactions, currency_profits, assets_sheet)

    # Profit per transaction
    # - Write each transaction to a new line in excel
    # - Write each transaction_profit to a new line in excel
    # TODO: Fix



    # Assets and total profit per currency
    # - Write each transaction to a new line in excel (debit/credit per currency)
    # - Write currency_profit per currency

    workbook.close()

    return None

def write_transactions_sheet(transactions, transactions_profits, sheet, format):
    
    
    # Write headers
    sheet.write('B2', "Transactions", format["sheet_header"])
    sheet.write('B4', "Date", format["column_header"])
    sheet.write('C4', "Currency Sold", format["column_header"])
    sheet.write('D4', "Amound Sold", format["column_header"])
    sheet.write('E4', "Price Sold", format["column_header"])
    sheet.write('F4', "Currency Bought", format["column_header"])
    sheet.write('G4', "Amount Bought", format["column_header"])
    sheet.write('H4', "Price Bought", format["column_header"])
    
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
        row += 1
    
    print('Transaction sheet completed.')    
    
    return None

def write_assets_sheet(transactions, currency_profits, sheet):
    
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


### Helper Methods ###
def initialize_workbook_and_worksheets():
    workbook = xlsxwriter.Workbook('tax_info.xlsx')
    transactions_sheet = workbook.add_worksheet('Transactions')
    assets_sheet = workbook.add_worksheet('Assets')
    
    return workbook, transactions_sheet, assets_sheet



### Testing ###

# Cleaned transactions: [transaction1, transaction2, ...]
# Cleaned transaction: [date, currency_sold, amount_sold, price_sold, currency_bought, amount_bought, price_bought]
cleaned_transaction_1 = ["01/01/2023", "BTC", 0.5, 25000, "USD", 12500, 1]
cleaned_transaction_2 = ["02/01/2023", "USD", 5000, 1, "USD", 0.25, 20000]
cleaned_transactions = [cleaned_transaction_1, cleaned_transaction_2]

transaction_profits = {"BTC": ["01/01/2023", 10000]}
currency_profits = {"BTC": 10000}

write_to_excel(cleaned_transactions, transaction_profits, currency_profits)





